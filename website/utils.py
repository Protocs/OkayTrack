from flask import session, redirect


def login_required(route):
    def decorated(*args, **kwargs):
        if "user_name" not in session:
            return redirect("/")
        route(*args, **kwargs)

    return decorated


PRIORITIES = ["Низкий приоритет", "Средний приоритет", "Высокий приоритет"]
STAGES = ["Начальный", "Основной", "Конечный"]
