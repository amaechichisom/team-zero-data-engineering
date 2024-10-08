import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch
from app import create_app  # Import your Flask app factory
from app.config.config import Config
from moto import mock_aws  # This will mock all AWS services
import boto3

@pytest.fixture
def client():
    app = create_app()  # Create a new instance of your Flask app
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_aws_s3():
    """Mock AWS S3 environment."""
    with mock_aws():
        conn = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
        yield conn

def test_upload_file(client, mock_aws_s3):
    data = {
        'recipient_name': 'John Doe',
        'file': (BytesIO(b"file content"), 'test.txt')
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 201
    assert b'File uploaded successfully' in response.data

def test_upload_file_missing_recipient(client):
    data = {
        'file': (BytesIO(b"file content"), 'test.txt')
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b'File or recipient name is missing' in response.data

def test_get_file(client, mock_aws_s3):
    # First, upload the file
    mock_aws_s3.put_object(Bucket=Config.S3_BUCKET, Key='test.txt', Body=b"file content")
    
    # Now, test retrieving the file
    response = client.get('/download/test.txt?recipient_name=John Doe')
    assert response.status_code == 200
    assert b'file_url' in response.data

def test_get_file_missing_recipient(client):
    response = client.get('/download/test.txt')
    assert response.status_code == 400
    assert b'Recipient name is missing' in response.data

def test_delete_file(client, mock_aws_s3):
    # First, upload the file
    mock_aws_s3.put_object(Bucket=Config.S3_BUCKET, Key='test.txt', Body=b"file content")
    
    # Now, test deleting the file
    response = client.delete('/delete/test.txt?recipient_name=John Doe')
    assert response.status_code == 200
    assert b'File deleted successfully' in response.data

def test_delete_file_missing_recipient(client):
    response = client.delete('/delete/test.txt')
    assert response.status_code == 400
    assert b'Recipient name is missing' in response.data
