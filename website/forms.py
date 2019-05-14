from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, EqualTo
from .db import User, Category


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Пароль (еще раз)",
                                   validators=[DataRequired(), EqualTo("password", "Пароли не совпадают")])
    submit = SubmitField("Войти")


class AddCategory(FlaskForm):
    name = StringField("Название категории")
    submit = SubmitField("Добавить")


class NewTaskForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    desc = TextAreaField("Описание", validators=[DataRequired()])
    # deadline = DateTimeField("Дата выполнения", validators=[DataRequired()])
    # performer = SelectField("Исполнитель", choices=[(user.name, user.name) for user in users])
    # category = SelectField("Категория", choices=([("", "-")] + [(c.id, c.name) for c in Category.query.all()]))
    tags = StringField("Теги (разделяйте запятыми)")
    submit = SubmitField("Создать")

