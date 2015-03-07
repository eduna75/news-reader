__author__ = 'justus'

from flask import Flask
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__, static_path='')
from app import views
from app import config_page

app.config.from_object(os.environ['APP_SETTINGS'])
Bootstrap(app)