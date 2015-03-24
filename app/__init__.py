__author__ = 'justus'

from flask import Flask
import os

app = Flask(__name__, static_path='')
from app import views
from app.backend.views import node as backend_node


app.register_blueprint(backend_node)
app.config.from_object(os.environ['APP_SETTINGS'])