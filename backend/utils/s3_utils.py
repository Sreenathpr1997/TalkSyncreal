import boto3
import os
from backend.config import AWS_BUCKET, AWS_REGION

s3 = boto3.client("s3", region_name=AWS_REGION)


def upload_file(file_path: str, key: str):

    s3.upload_file(
        file_path,
        AWS_BUCKET,
        key
    )


def download_file(key: str, destination: str):

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    s3.download_file(
        AWS_BUCKET,
        key,
        destination
    )