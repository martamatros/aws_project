from botocore.exceptions import ClientError
from flask import Flask, render_template, request
import boto3
from botocore.config import Config
import config
import uuid
from datetime import datetime

s3_resource = boto3.resource(
  's3',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2'
) 

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

db_client = boto3.client(
  'dynamodb',
  aws_access_key_id = config.ACCESS_KEY,
  aws_secret_access_key = config.SECRET_KEY,
  region_name='us-east-2',
  )

app = Flask(__name__)

@app.route("/")
def main():
  response = s3_client.generate_presigned_post(Bucket='mmatros', Key='uploads/${filename}', Fields={}, Conditions=[{"success_action_redirect": "http://ec2-18-216-129-165.us-east-2.compute.amazonaws.com/success"}],ExpiresIn=604800)
  return render_template('index.html', config=config, data=response)

@app.route("/success")
def success():
  if request.args.get('key'):
    send_logs_to_db('upload to s3', request.args.get('key'))
  return render_template('success.html')

@app.route('/images', methods=['GET', 'POST'])
def list_of_images():
  bucket = s3_resource.Bucket('mmatros')
  images = []

  for file in bucket.objects.all():
    if file.key[-1] != "/":
      url = s3_client.generate_presigned_url('get_object', Params={'Bucket': 'mmatros', 'Key': file.key,}, ExpiresIn=604800)
      images.append({'key': file.key, 'url': url })

  return render_template('images.html', images=images)

@app.route("/transform", methods=['GET', 'POST'])
def transform():
  send_images_to_queue = request.form.getlist('imagesSelection')

  entries = []
  message_group_id = str(uuid.uuid4())
  for item in send_images_to_queue:
    entries.append({
      'Id': str(uuid.uuid4()),
      'MessageBody': item,
      'MessageDeduplicationId': str(uuid.uuid4()),
      'MessageGroupId': message_group_id,
    })
  response = sqs.send_message_batch(
      QueueUrl='https://sqs.us-east-2.amazonaws.com/333651036015/awsprojekt.fifo',
      Entries=entries,
  )

  return render_template('transform.html')

def send_logs_to_db(action, file):
  print(str(datetime.now()))
  db_client.put_item(
    TableName='logs',
    Item={
        'logId': { "S": str(uuid.uuid4())},
        'action': { "S": action},
        'file': { "S": file},
        'date': { "S": str(datetime.now())},
    },
  )

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, use_reloader=True)