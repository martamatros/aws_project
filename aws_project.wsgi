import os, sys
sys.path.insert(0, '/var/www/html/aws_project')



for key in ['ACCESS_KEY', 'SECRET_KEY']:
  os.environ[key] = environ.get(key, '')
  
from aws_project import app as application
