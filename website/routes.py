from flask import render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from website.app import app, bot
from website.db import User, db
from website.forms import LoginForm, RegisterForm
from website.utils import login_required


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.login.data)
        if user is None:
            form.login.errors.append("Такого пользователя не существует")
            return render_template("login.html", form=form)
        if not check_password_hash(user.password_hash, form.password.data):
            form.password.errors.append("Неправильный пароль")
            return render_template("login.html", form=form)
        session["user_name"] = user.name
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.login.data)
        if user is not None:
            form.login.errors.append("Пользователь с таким логином уже существует")
            return render_template("register.html", form=form)
        user = User(name=form.login.data, password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        session["user_name"] = user.name
        return redirect("/")

    return render_template("register.html", form=form)


@login_required
@app.route("/logout")
def logout():
    del session["user_name"]
    return redirect("/")


@app.route("/post", methods=["POST"])
def get_request():
    return bot.handle_request(request.json)
