import json

from .res_req_parser import RequestParser, ResponseParser
from .session import Session


class Bot:
    """Ядро навыка для приложения ``app``"""

    def __init__(self, app):
        self.app = app
        self._sessions = {}

    def handle_request(self, req_json):
        request = RequestParser(req_json)
        response = ResponseParser(request)

        # Создание сессии для нового пользователя
        user_id = request.session["user_id"]
        if user_id not in self._sessions or request.new_session:
            self._create_new_session(request, user_id)

        session = self._sessions[user_id]
        session.handle_state(request, response)
        return json.dumps(response)

    def _create_new_session(self, request, user_id):
        from website.db import User

        user = User.query.filter_by(alice_id=user_id).first()
        if user is None:
            self._sessions[user_id] = Session(None)
            return
        self._sessions[user_id] = Session(user)
