from flask import Flask
from .config import FORM_SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = FORM_SECRET_KEY
app.config["JSON_AS_ASCII"] = False
