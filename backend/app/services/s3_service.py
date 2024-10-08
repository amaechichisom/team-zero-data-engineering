
from boto3 import client
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from app.config.config import Config

class S3Service:
    """Service for interacting with AWS S3."""
    
    def __init__(self):
        self.s3_client = client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
        self.aws_access_key_id = Config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        self.bucket_name = Config.S3_BUCKET

    def upload_file(self, file, filename):
        """Uploads a file to the configured S3 bucket."""
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, filename)
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise e

    def generate_file_url(self, filename):
        """Generates a public URL for the given file."""
        return f"https://{self.bucket_name}.s3.{Config.AWS_REGION}.amazonaws.com/{filename}"

    def delete_file(self, filename):
        """Deletes a file from the S3 bucket."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
        except Exception as e:
            raise e
