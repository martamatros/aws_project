import boto3
# import config

from flask import Flask, render_template


app = Flask(__name__)
@app.route("/")

def main():
  return render_template('index.html')

@app.route('/images')
def list_of_images():
  return render_template('images.html')
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)