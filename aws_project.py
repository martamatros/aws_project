import boto3
from botocore.exceptions import ClientError
import logging

from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")

def main():
  s3 = boto3.client('s3')
  try:
    response = s3.generate_presigned_post(Bucket='aws-projekt', Key='uploads/${filename}', Fields={}, Conditions=[],ExpiresIn=2592000)
    return render_template('index.html', config=response)
  except ClientError as e:
    logging.error(e)
    return render_template('index.html', config='')

@app.route('/images')
def list_of_images():
  return render_template('images.html')
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
