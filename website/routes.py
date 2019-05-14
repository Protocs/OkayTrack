from flask import render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from website.app import app, bot
from website.db import User, db, Category, Task
from website.forms import LoginForm, RegisterForm, AddCategory
from website.utils import login_required


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


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
        session["role"] = user.role
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
        session["role"] = user.role
        return redirect("/")

    return render_template("register.html", form=form)


@login_required
@app.route("/logout")
def logout():
    del session["user_name"]
    del session["role"]
    return redirect("/")


@app.route("/post", methods=["POST"])
def get_request():
    return bot.handle_request(request.json)


@app.route("/task-categories")
def task_categories():
    if session["role"] != "admin":
        return redirect("/")

    categories = Category.get_all()
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if session["role"] != "admin":
        return redirect("/")

    form = AddCategory()
    if form.validate_on_submit():
        category = Category.get_by_name(form.name.data)
        if category is not None:
            form.name.errors.append("Категория с таким названием уже существует")
            return render_template("add_or_edit_category.html", form=form)
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect("/task-categories")
    return render_template("add_or_edit_category.html", form=form)


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if session["role"] != "admin":
        return redirect("/")

    category = Category.get_by_id(category_id)
    if category is None:
        return redirect("/task-categories")
    form = AddCategory()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        return redirect("/task-categories")
    return render_template("add_or_edit_category.html", category=category, form=form)


@app.route("/users", methods=["GET", "POST"])
def users():
    if session["role"] != "admin":
        return redirect("/")

    if request.method == "POST":
        for k in request.form:
            username = "-".join(k.split("-")[1])
            user = User.get_by_username(username)
            if k.startswith("status"):
                user.blocked = not user.blocked
            elif k.startswith("setadmin"):
                user.role = "admin" if user.role == "user" else "user"
            db.session.commit()

    users = User.get_all()
    return render_template("users.html", users=users)
