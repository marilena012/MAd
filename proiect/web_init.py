import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'mla'

web_app = Flask(__name__, instance_path=os.path.join(os.getcwd()))

web_app.secret_key = 'PASSWORD'
web_app.root_path = os.path.join(os.getcwd())
print(web_app.root_path)
