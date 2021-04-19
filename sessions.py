import secrets


class SessionManager:
    def __init__(self):
        # sessionId: userId
        self._data = {}
    
    def get_user_id(self, session_id):
        return self._data.get(session_id)
    
    def create_session(self, user_id):
        token = secrets.token_hex(16)
        self._data[token] = user_id
        return token

    def delete_session(self, session_id):
        self._data[session_id] = None
