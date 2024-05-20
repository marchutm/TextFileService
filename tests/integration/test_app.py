import pytest
from flask.testing import FlaskClient
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', ))
sys.path.insert(0, project_root)

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'File Upload' in response.data
    assert b'<form method="POST" action="" enctype="multipart/form-data">' in response.data
    assert b'<input type="file" name="file" multiple>' in response.data
    assert b'<input type="submit" value="Submit">' in response.data


def test_upload_valid_txt_file(client: FlaskClient):
    with open('tests/integration/test_files/example.txt', 'rb') as f:
        data = {'file': (f, 'example.txt')}
        response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'text_statistics' in response.data
    assert b'language' in response.data
    assert b'emails' in response.data
    assert b'letter_frequency' in response.data


def test_upload_valid_csv_file(client: FlaskClient):
    with open('tests/integration/test_files/waterquality.txt', 'rb') as f:
        data = {'file': (f, 'waterquality.csv')}
        response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'num_rows' in response.data
    assert b'num_cols' in response.data
    assert b'columns_list' in response.data
    assert b'unique_values' in response.data
    assert b'statistics' in response.data


def test_upload_valid_json_file(client: FlaskClient):
    with open('tests/integration/test_files/customers.json', 'rb') as f:
        data = {'file': (f, 'customers.json')}
        response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'num_elements' in response.data
    assert b'keys_list' in response.data
    assert b'keys_per_element' in response.data
    assert b'missing_values' in response.data


def test_upload_invalid_file_extension(client: FlaskClient):
    with open('tests/integration/test_files/invalid_file.exe', 'rb') as f:
        data = {'file': (f, 'invalid_file.exe')}
        response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Bad Request' in response.data


def test_metrics_endpoint(client: FlaskClient):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'flask_app_requests_total' in response.data
    assert b'flask_app_errors_total' in response.data
    assert b'flask_app_text_files_total' in response.data
    assert b'flask_app_request_latency_seconds' in response.data
    assert b'flask_app_file_size_bytes' in response.data
