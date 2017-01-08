from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import logging, sys

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
mail = Mail(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from app import views, models