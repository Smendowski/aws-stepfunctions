import json
import boto3
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


def lambda_handler(event, context):
    s3_uri = event['body']['location']
    embedding_config = event['body']['configuration']['embedding']
    n_components = embedding_config['t-SNE']['parameters']['n_components']
    perplexity = embedding_config['t-SNE']['parameters']['perplexity']

    data: np.ndarray =  _download_data_from_s3(s3_uri)
    
    tsne_embedding = TSNE(
        n_components=n_components,
        perplexity=perplexity
    ).fit_transform(data)

    configuration = event['body']['configuration']
    del configuration['embedding']

    return {
        'statusCode': 200,
        'body': {
            'location': s3_uri,
            'configuration': configuration
        }
    }
