import json
import boto3
from time import perf_counter
import numpy as np
from io import BytesIO
from urllib.parse import urlparse
from sklearn.manifold import TSNE

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


def lambda_handler(event, context) -> str:
    embedding_config = event['embedding']
    technique = list(embedding_config.keys())[0]
    n_components = embedding_config[technique]['parameters']['n_components']
    perplexity = embedding_config[technique]['parameters']['perplexity']

    s3_uri = event['workflow_results']['raw_data_location']

    data: np.ndarray =  _download_data_from_s3(s3_uri)
    
    start = perf_counter()
    _ = TSNE(
        n_components=n_components,
        perplexity=perplexity
    ).fit_transform(data)
    elapsed_time = perf_counter() - start

    return f"{elapsed_time:.2f} seconds"
