import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class to handle AWS and S3 settings."""
    
    S3_BUCKET = os.getenv('S3_BUCKET', 'datathon-zero')
    S3_REGION = os.getenv('AWS_REGION', 'your-region')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID','AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY','AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'your-region')
    
    def validate():
        if not all([Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY, Config.S3_BUCKET]):
            raise ValueError("AWS credentials or S3 Bucket name are missing in the environment variables.")