from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)

from app import views
from app.backend.views import node as backend_node


app.register_blueprint(backend_node)
app.config.from_object(os.environ['APP_SETTINGS'])


from app.models import *
