import boto3
from botocore.exceptions import ClientError
import logging
import os
from flask import Flask, render_template

import config

app = Flask(__name__)
@app.route("/")



def main():
  s3_resource = boto3.resource(
    's3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY,
  ) 
  s3_client = boto3.client(
    's3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY,
  )

  response = s3_client.generate_presigned_post(Bucket='aws-projekt', Key='uploads/${filename}', Fields={}, Conditions=[],ExpiresIn=2592000)
  return render_template('index.html', config=response)

@app.route('/images')
def list_of_images():
  s3_resource = boto3.resource(
    's3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY,
  ) 
  s3_client = boto3.client(
    's3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY,
  )
  bucket = s3_resource.Bucket('aws-projekt')
  bucketname = 'aws-projekt' # replace with your bucket name
  # s3 = boto3.resource('s3')
  # s3.Bucket(bucketname).download_file(filename, 'my_localimage.jpg')

  images = []

  for file in bucket.objects.all():
    url = s3_client.generate_presigned_url('get_object', Params={'Bucket': 'aws-projekt', 'Key': file.key,}, ExpiresIn=3600)
    # url = s3_client.Bucket(bucketname).download_file(file.key, 'my_localimage.jpg')
    images.append(url)
    print(url)


  return render_template('images.html', images=images)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, use_reloader=True)