TYPICAL_RESPONSE = {
    "session": None,
    "version": None,
    "response": {"end_session": False},
}


class RequestParser(dict):
    def __init__(self, request_json):
        super().__init__(request_json)

    @property
    def session(self):
        return self.get("session")

    @property
    def version(self):
        return self.get("version")

    @property
    def text(self):
        return self["request"].get("original_utterance")

    @property
    def new_session(self):
        return self.session["new"]

    @property
    def user_id(self):
        return self.session["user_id"]


class ResponseParser(dict):
    def __init__(self, request: RequestParser):
        super().__init__()
        self._construct_response_params(request)

    def _construct_response_params(self, request):
        for k, v in TYPICAL_RESPONSE.items():
            if k in ("session", "version"):
                self[k] = request.get(k)
            else:
                self[k] = v

    @property
    def reply_text(self):
        return self["response"]["text"]

    @reply_text.setter
    def reply_text(self, new_text):
        self["response"]["text"] = new_text

    @property
    def end_session(self):
        return self["response"]["end_session"]

    @end_session.setter
    def end_session(self, end):
        self["response"]["end_session"] = end

    @property
    def buttons(self):
        return self["response"]["buttons"]

    @buttons.setter
    def buttons(self, new_buttons):
        self["response"]["buttons"] = new_buttons
