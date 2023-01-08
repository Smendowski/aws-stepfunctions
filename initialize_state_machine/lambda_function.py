import json
import boto3
from datetime import datetime
import uuid

s3Client = boto3.client('s3')
client = boto3.client('stepfunctions')

SM_NAME: str = 'Large-Scale-Computing-Project'
SM_ARN: str = f'arn:aws:states:us-east-1:968167118559:stateMachine:{SM_NAME}'


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3Client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')

    transactionId = str(uuid.uuid1())
    input = {'TransactionId': transactionId, 'Type': 'PURCHASE'}
    input.update({'data': data})

    response = client.start_execution(
        stateMachineArn=SM_ARN,
        name=transactionId,
        input=json.dumps(input)
    )
