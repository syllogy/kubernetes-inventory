#!/usr/bin/env python3 
import os
import boto3
from botocore.config import Config

CLUSTER = os.getenv('CLUSTER')
BUCKET = os.getenv('S3_BUCKET')
FOLDER = os.getenv('S3_FOLDER')
PROXY = os.getenv('PROXY')
REGION = os.getenv('S3_REGION')

proxy_definitions = {
    'http': PROXY,
    'https': PROXY
}

my_config = Config({
    'region_name': REGION,
    'signature_version': 'v4',
    'proxies': proxy_definitions
})


s3 = boto3.client('s3')
print(f'push s3://{BUCKET}/{FOLDER}/{CLUSTER}.json')
s3.upload_file('inventory.json', BUCKET, f'{FOLDER}/{CLUSTER}.json')

