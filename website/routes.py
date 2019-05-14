from flask import render_template

from website.app import app
from website.db import User


@app.route("/")
def index():
    return render_template("index.html")
