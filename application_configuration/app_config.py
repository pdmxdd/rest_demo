import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# DB URI is set with Environment Variables
app.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}:{}/{}'.format(os.environ['DB_TYPE'], os.environ['DB_USER'], os.environ['DB_PASS'], os.environ['DB_HOST'], os.environ['DB_PORT'], os.environ['DB_NAME'])
db = SQLAlchemy(app)
