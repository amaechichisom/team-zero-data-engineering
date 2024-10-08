from unittest import TestCase
from unittest.mock import patch, MagicMock
import pytest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from io import BytesIO
from app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError

class TestS3Service(TestCase):

    @patch('boto3.client')
    def test_upload_file(self, mock_boto_client):
        # Create a mock S3 client
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Initialize S3 service
        s3_service = S3Service()

        # Simulate a file upload
        file = BytesIO(b"file content")
        filename = "test_file.txt"

        # Call upload_file method
        s3_service.upload_file(file, filename)

        # Assert that upload_fileobj was called once
        mock_s3.upload_fileobj.assert_called_once_with(file, s3_service.bucket_name, filename)

    @patch('boto3.client')
    def test_upload_file_with_invalid_credentials(self, mock_boto_client):
        # Simulate the NoCredentialsError
        mock_boto_client.side_effect = NoCredentialsError

        s3_service = S3Service()

        # Assert that NoCredentialsError is raised when trying to upload a file
        with self.assertRaises(NoCredentialsError):
            s3_service.upload_file(BytesIO(b"content"), "file.txt")

    @patch('boto3.client')
    def test_delete_file(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        s3_service = S3Service()
        
        # Call delete_file method
        filename = "test_file.txt"
        s3_service.delete_file(filename)

        # Assert that delete_object was called once
        mock_s3.delete_object.assert_called_once_with(Bucket=s3_service.bucket_name, Key=filename)
