import json
import boto3
from datetime import datetime
import uuid
import yaml

s3Client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = 'lsc-stepfunctions-project'
    key = 'params.yaml'

    response = s3Client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    data = yaml.safe_load(data)

    return data
