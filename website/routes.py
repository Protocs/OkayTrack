from flask import render_template, request

from website.app import app, bot
from website.db import User
from website.forms import LoginForm, RegisterForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        ...


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "GET":
        return render_template("register.html", form=form)
    else:
        ...


@app.route("/post", methods=["POST"])
def get_request():
    return bot.handle_request(request.json)
