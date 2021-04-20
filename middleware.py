from werkzeug.wrappers import Request
from sessions import SessionManager


class AuthenticationMiddleware:
    def __init__(self, app, db, session_manager: SessionManager):
        self.app = app
        self.db = db
        self.session_manager = session_manager

    def __call__(self, environ, start_response):
        request = Request(environ)
        session_id = request.cookies.get('sessionID')
        if session_id:
            user_id = self.session_manager.get_user_id(session_id)
            user = self.db.get_user_by_id(user_id)
            environ['user'] = user
        else:
            environ['user'] = None

        return self.app(environ, start_response)
