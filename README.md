# Text File Processing Service

## 1. Introduction

The Text File Processing Service allows users to upload text files in CSV, TXT, or JSON formats, which are then processed, and their summaries are saved in JSON files. Additionally, the service collects metrics related to the number of processed files, processing time, and size of uploaded files.

## 2. Installation and Running

### 2.1 Prerequisites

- Python 3.x
- Libraries listed in the `requirements.txt` file

### 2.2 Installation Instructions

1. Download the source code from the repository.
2. Install the required libraries using the command `pip install -r requirements.txt`.
3. Run the application using the command `python app.py`.

## 3. Interaction with the Service

### 3.1 File Upload

1. Go to the homepage of the application.
2. Click the "Choose File" button and select the file you want to process.
3. Click the "Upload File" button.
4. After processing the file, a JSON file with the summary data will be generated, which will be available for download.

## 4. Configuration

### 4.1 Configuration Parameters

- `MAX_CONTENT_LENGTH`: Maximum allowable size of uploaded files (in bytes).
- `UPLOAD_EXTENSIONS`: List of allowable file extensions.
- `UPLOAD_PATH`: Path to the directory where uploaded files will be stored.
- `SUMMARY_PATH`: Path to the directory where files with data summaries will be stored.

## 5. Error Handling

- Errors related to uploaded files (e.g., disallowed extension, exceeding maximum size) generate appropriate HTTP error codes.
- In case of other errors, the user will receive an error message, and a server error will be displayed.

## 6. Metrics Documentation

### 6.1 Metrics Collected by the Service

- `flask_app_requests_total`: Total number of requests to the service.
- `flask_app_errors_total`: Total number of errors occurring in the service.
- `flask_app_text_files_total`: Total number of processed text files, divided by file type.
- `flask_app_request_latency_seconds`: Processing time of a single request in seconds.
- `flask_app_file_size_bytes`: Size of uploaded files, divided by file type.

### 6.2 Access to Metrics

- Metrics are available at the address `/metrics`.
- To make metrics available, you need to run the Prometheus program using the command `./prometheus --config.file=prometheus.yml`.
- Metrics will be available at the address http://localhost:9090.

## 7. Development and Contribution

- The project is open to community contributions.
- Report bugs and propose new features through the issue tracking system in the repository.

## 8. License

All rights reserved.
