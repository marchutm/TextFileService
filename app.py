from flask import Flask, render_template, request, redirect, url_for, abort, send_file
import os
from werkzeug.utils import secure_filename
import mimetypes
from TextFileProcessor import TextFileProcessor
from CSVFileProcessor import CSVFileProcessor
from JSONFileProcessor import JSONFileProcessor
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Gauge
import json
import io
import time

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.txt', '.json']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SUMMARY_PATH'] = 'summaries'

request_counter = Counter('flask_app_requests_total', 'Total number of requests')
error_counter = Counter('flask_app_errors_total', 'Total number of errors')
file_counter = Counter('flask_app_text_files_total', 'Total number of text files processed', ['file_type'])
request_latency = Gauge('flask_app_request_latency_seconds', 'Request latency in seconds')
file_size = Gauge('flask_app_file_size_bytes', 'Size of uploaded files in bytes', ['file_type'])


def validate_file(filename):
    mime_type = mimetypes.MimeTypes().guess_type(filename)
    if mime_type[0] == 'text/plain':
        return '.txt'
    elif mime_type[0] == 'text/csv':
        return '.csv'
    elif mime_type[0] == 'application/json':
        return '.json'
    else:
        return None


async def process_file(uploaded_file, filename, file_ext):
    total_bytes = 0
    uploaded_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    with open(uploaded_file_path, 'wb') as f:
        for chunk in uploaded_file:
            f.write(chunk)
            total_bytes += len(chunk)
    file_size.labels(file_type=file_ext).set(total_bytes)

    summary = None
    if file_ext == '.txt':
        file_counter.labels(file_type='txt').inc()
        text_processor = TextFileProcessor(uploaded_file_path)
        summary = text_processor.get_data_summary()

    if file_ext == '.csv':
        file_counter.labels(file_type='csv').inc()
        csv_processor = CSVFileProcessor(uploaded_file_path)
        summary = csv_processor.get_data_summary()

    if file_ext == '.json':
        file_counter.labels(file_type='json').inc()
        json_processor = JSONFileProcessor(uploaded_file_path)
        summary = json_processor.get_data_summary()

    if summary:
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        summary_filename = os.path.join(app.config['SUMMARY_PATH'], f'summary_{base_filename}.json')
        with io.open(summary_filename, 'w', encoding="utf-8-sig") as json_file:
            json.dump(summary, json_file, ensure_ascii=False)
        return summary_filename


@app.route('/')
def index():
    request_counter.inc()
    return render_template('index.html')


@app.route('/', methods=['POST'])
async def upload_files():
    request_counter.inc()
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_file(filename):
            error_counter.inc()
            abort(400)

        if len(uploaded_file.read()) > app.config['MAX_CONTENT_LENGTH']:
            error_counter.inc()
            abort(413)

        start_time = time.time()

        try:
            summary_filename = await process_file(uploaded_file, filename, file_ext)
        except Exception as e:
            error_counter.inc()
            print(f"Error processing file: {e}")
            abort(500)

        end_time = time.time()
        request_latency.set(end_time - start_time)

        return send_file(summary_filename, as_attachment=True)

    return redirect(url_for('index'))


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(debug=True)
