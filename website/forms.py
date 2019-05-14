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
    tags = StringField("Теги (разделяйте запятыми)")
    submit = SubmitField("Создать")


class CommentForm(FlaskForm):
    comment = TextAreaField(validators=[DataRequired("Введите текст комментария")])
    submit = SubmitField("Отправить")
