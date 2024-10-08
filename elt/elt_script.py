import os
import pandas as pd
import boto3
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Environment variables
S3_BUCKET_NAME = os.getenv('S3_BUCKET', 'datathon-zero')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'elt_postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')

# S3 client setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# SQLAlchemy connection string for PostgreSQL
postgres_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
engine = create_engine(postgres_url)

def fetch_csv_files_from_s3(bucket_name):
    """Fetches all CSV files from the specified S3 bucket"""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print(f"No files found in the bucket: {bucket_name}")
            return []
        
        csv_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.csv')]
        return csv_files
    except Exception as e:
        print(f"Error fetching files from S3: {e}")
        return []

def load_csv_to_postgres(file_key):
    """Loads a CSV file from S3 into PostgreSQL"""
    try:
        # Fetch file from S3
        csv_obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
        csv_data = pd.read_csv(csv_obj['Body'])

        if csv_data.empty:
            print(f"{file_key} is empty, skipping.")
            return

        # Convert unsigned 64-bit integers to a supported type (e.g., int64 or str)
        for col in csv_data.columns:
            if csv_data[col].dtype == 'uint64':
                print(f"Converting column {col} from uint64 to int64.")
                csv_data[col] = csv_data[col].astype('int64')  # or use .astype('str') if you want to convert to string

        # Load data into PostgreSQL
        table_name = file_key.replace('.csv', '')  # Adjust table naming logic as needed
        csv_data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Loaded {file_key} into table {table_name}")
    
    except pd.errors.EmptyDataError:
        print(f"CSV file {file_key} is empty. Skipping.")
    except SQLAlchemyError as e:
        print(f"Error loading data into PostgreSQL: {e}")
    except ValueError as ve:
        print(f"Error processing {file_key}: {ve}")
    except Exception as e:
        print(f"Error processing {file_key}: {e}")


def run_elt():
    """Main ELT script execution"""
    print(f"Fetching CSV files from S3 bucket: {S3_BUCKET_NAME}")
    
    csv_files = fetch_csv_files_from_s3(S3_BUCKET_NAME)
    
    if not csv_files:
        print("No CSV files found.")
        return
    
    for file_key in csv_files:
        print(f"Processing file: {file_key}")
        load_csv_to_postgres(file_key)

if __name__ == "__main__":
    run_elt()
