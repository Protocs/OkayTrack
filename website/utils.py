from flask import session, redirect
import uuid


def login_required(route):
    def decorated(*args, **kwargs):
        if "user_name" not in session:
            return redirect("/")
        route(*args, **kwargs)

    return decorated


def check_token():
    ...


def generate_token():
    return uuid.uuid4()


PRIORITIES = ["Низкий приоритет", "Средний приоритет", "Высокий приоритет"]
STAGES = ["Начальный", "Основной", "Конечный"]
