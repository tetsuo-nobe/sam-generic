import json
import boto3
import datetime
import os
from botocore.config import Config
from aws_xray_sdk.core import patch
patch(['boto3'])

# import requests
dynamodb = boto3.resource('dynamodb', region_name="ap-northeast-1")
sqs = boto3.resource('sqs')
s3  = boto3.resource('s3')

def lambda_handler(event, context):
    qname = os.getenv('SQS_QUEUE')
    table_name = os.getenv('DDB_TABLE')

    #print(event)
    req_id = context.aws_request_id
    body = json.loads(event['body'])
    bucketName = body['bucket']
    keyName    = body['key']
    #print('--------------------------------')
    print(bucketName)
    print(keyName)
    
    # S3バケットからオブジェクト取得
    bucket = s3.Bucket(bucketName)              # S3バケット取得
    file_path= "/tmp/dwnld.txt"             # ダウンロードするオブジェクトのファイルパスを指定
    bucket.download_file(keyName, file_path)    # ダウンロード実行
    # ファイルの内容を取得
    f = open('/tmp/dwnld.txt', 'r', encoding='UTF-8')
    data = f.read()
    print(data)
    f.close()
    
    # キューの名前を指定してインスタンスを取得
    queue = sqs.get_queue_by_name(QueueName=qname)
    queue.send_message(MessageBody=data)
    
    # DynamoDBへput_item実行
    now = str(datetime.datetime.now())
    table = dynamodb.Table(table_name)
    response = table.put_item(
       Item={
            'id': req_id,
            'bucket': bucketName,
            'objectkey': keyName,
            'datetime': now
        }
    )
    #
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done:"+ bucketName + ":" + keyName,
            # "location": ip.text.replace("\n", "")
        }),
    }
