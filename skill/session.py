from werkzeug.security import check_password_hash


class Session:
    def __init__(self, user):
        self._user = user
        if not self._user:
            self._current_state = 'LOGIN'
        else:
            self._current_state = 'GREETING'

    def handle_state(self, req_parser, resp_parser):
        from website.db import db, User
        if self._current_state == 'GREETING':
            self.greet(resp_parser)
        elif self._current_state == 'LOGIN':
            resp_parser.reply_text = 'Введите Ваше имя и пароль'
            self._current_state = 'CHECK_LOGIN'
        elif self._current_state == 'CHECK_LOGIN':
            try:
                login, password = req_parser.text.split()
                user = User.get_by_username(login)
                if not user:
                    resp_parser.reply_text = 'Такого пользователя не существует. ' \
                                             'Попробуйте еще раз'
                else:
                    if check_password_hash(user.password_hash, password):
                        user.alice_id = req_parser.user_id
                        db.session.commit()
                        self._current_state = 'GREETING'
                        self.greet(resp_parser)
                    else:
                        resp_parser.reply_text = 'Неверный пароль. Попробуйте еще раз'
            except ValueError:
                resp_parser.reply_text = 'Неверное количество слов. ' \
                                         'Попробуйте еще раз'
        elif self._current_state == 'CHOOSE':
            pass

    def greet(self, resp_parser):
        resp_parser.reply_text = 'Добро пожаловать в систему! ' \
                                 'Вам доступны следующие команды:\n' \
                                 '1. Покажи мои задачи\n' \
                                 '2. Покажи просроченные задачи\n' \
                                 '3. Добавить задачу\n' \
                                 '4. Покажи задачу номер id_задачи\n' \
                                 '5. Назначить задачу id_задачи пользователю имя_пользователя\n' \
                                 '6. Начать задачу id_задачи\n'
        resp_parser.buttons = [{'title': 'Покажи мои задачи',
                                'hide': False},
                               {'title': 'Покажи просроченные задачи',
                                'hide': False},
                               {'title': 'Добавить задачу',
                                'hide': False}]
        self._current_state = 'CHOOSE'
