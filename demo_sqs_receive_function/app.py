import json
import boto3
import datetime
import os
from botocore.config import Config
from aws_xray_sdk.core import patch
patch(['boto3'])

def lambda_handler(event, context):
    print(event)
    #
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done"
        }),
    }
