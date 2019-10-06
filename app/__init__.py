from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static/')
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from app import views
from app.backend.views import node as backend_node


app.register_blueprint(backend_node)


from app.models import *