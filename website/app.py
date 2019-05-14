from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .config import *
from skill.bot import Bot

app = Flask(__name__)
app.config["SECRET_KEY"] = FORM_SECRET_KEY
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TRACK_MODIFICATIONS

db = SQLAlchemy(app)
bot = Bot(app)
api = Api(app)