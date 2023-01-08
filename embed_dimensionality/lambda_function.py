import json
import boto3
import numpy as np
from io import BytesIO
from urllib.parse import urlparse

s3_client = boto3.client('s3')


def _download_data_from_s3(s3_uri: str) -> np.ndarray:
    bytes_ = BytesIO()
    parsed_s3 = urlparse(s3_uri)
    s3_client.download_fileobj(
        Fileobj=bytes_,
        Bucket=parsed_s3.netloc,
        Key=parsed_s3.path[1:]
    )
    bytes_.seek(0)

    return np.load(bytes_, allow_pickle=True)

def lambda_handler(event, context):
    s3_bucket = 'lsc-stepfunctions-project'
    s3_key = 'mnist'
    s3_uri = f"s3://{s3_bucket}/{s3_key}"

    data: np.ndarray =  _download_data_from_s3(s3_uri)
    return f"Data with {data.shape} shape downloaded from {s3_uri}"
