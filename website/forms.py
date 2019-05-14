from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


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
