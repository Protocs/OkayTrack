from telegram.ext import Updater, CommandHandler
from werkzeug.security import check_password_hash

from website.db import User, db, Task
import logging

logging.basicConfig(level=logging.DEBUG)


def check_user(update):
    user_id = update.message.from_user.id
    user = User.get_by_telegram_id(user_id)
    return user


def auth(bot, update, args):
    if len(args) != 2:
        update.message.reply_text("Неверное количество аргументов")
    else:
        login, password = args[0], args[1]
        user = User.get_by_username(login)
        if user is None:
            update.message.reply_text("Такого пользователя не существует")
            return
        if check_password_hash(user.password_hash, password):
            update.message.reply_text("Авторизация успешная")
            user.telegram_id = update.message.from_user.id
            db.session.commit()
        else:
            update.message.reply_text("Неверный пароль")


def task(bot, update):
    user = check_user(update)
    if user:
        tasks = Task.get_user_tasks(user.name)
        text = ""
        for task in tasks:
            text += f"Задача №{task.id}\n"
            text += f"Название: {task.name}\n"
            text += f"Дедлайн: {task.deadline}\n"
            text += "\n\n"
        update.message.reply_text(text)
    else:
        update.message.reply_text("Авторизуйтесь")


def main():
    updater = Updater("887196769:AAHEEEE-VdWhEuZKbuFH5NxmsXC_eD2S3Bs")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("auth", auth, pass_args=True))
    dp.add_handler(CommandHandler("task", task))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
