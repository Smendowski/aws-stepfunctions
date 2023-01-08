import json
import boto3
import numpy as np
import sklearn.datasets
from io import BytesIO
from urllib.parse import urlparse

s3_client = boto3.client('s3')

def _upload_data_to_s3(data: np.ndarray, s3_uri: str) -> None:
    bytes_ = BytesIO()
    np.save(bytes_, data, allow_pickle=True)
    bytes_.seek(0)
    parsed_s3 = urlparse(s3_uri)
    s3_client.upload_fileobj(
        Fileobj=bytes_,
        Bucket=parsed_s3.netloc,
        Key=parsed_s3.path[1:]
    )


def lambda_handler(event, context) -> str:
    dataset_config = event['dataset']
    dataset_name: str = list(dataset_config.keys())[0]
    n_rows: int = dataset_config[dataset_name]['parameters']['rows']

    dataset = sklearn.datasets.fetch_openml(
        dataset_name,
        data_home='/tmp/sklearn'
    )
    data = dataset.data
    data = data[:n_rows]

    s3_bucket = 'lsc-stepfunctions-project'
    s3_key = 'mnist'
    s3_uri = f"s3://{s3_bucket}/{s3_key}"

    _upload_data_to_s3(data, s3_uri)

    return s3_uri
