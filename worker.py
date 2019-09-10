from PIL import Image
import boto3
from botocore.config import Config
import config
import uuid

s3_client = boto3.client(
  's3',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2',
  config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4')
)

sqs = boto3.client(
  'sqs',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2',
)

s3_resource = boto3.resource(
  's3',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2'
) 

db_client = boto3.client(
  'dynamodb',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2',
)

def send_logs_to_db(action, file):
  db_client.put_item(
    TableName='logs',
    Item={
        'logId': { "S": str(uuid.uuid4())},
        'action': { "S": action},
        'file': { "S": file},
    },
  )

while True:
  response = sqs.receive_message(QueueUrl='https://sqs.us-east-2.amazonaws.com/333651036015/awsprojekt.fifo',MaxNumberOfMessages=10, VisibilityTimeout=30) 
  if response['Messages']:
    for message in response['Messages']:
      print(message['Body'])
      s3_resource.Object('mmatros', message['Body']).download_file(message['Body'])
      img = Image.open(message['Body'])
      img.resize((int(round(img.size[0]*0.5)), int(round(img.size[1]*0.5)))).save(message['Body'])
      s3_resource.Object('mmatros', message['Body']).upload_file(message['Body'])
      sqs.delete_message(QueueUrl='https://sqs.us-east-2.amazonaws.com/333651036015/awsprojekt.fifo', ReceiptHandle=message['ReceiptHandle'])
      send_logs_to_db('transform image', message['Body'])


