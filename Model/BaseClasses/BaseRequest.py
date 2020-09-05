import uuid
from tornado.web import RequestHandler
from tornado.concurrent import Future
from SharedData import SharedData


class BaseRequestHandler(RequestHandler):
    def __init__(self, app, request, **kwargs):
        super().__init__(app, request, **kwargs)
        self.session_id = self.get_cookie("sessionId")

    def prepare(self):
        if not self.session_id or not SharedData().is_online(self.session_id):
            self.session_id = uuid.uuid4().hex
            self.set_cookie("sessionId", self.session_id)
            SharedData().add_online(self.session_id)

        if not self.current_user and self.request.uri.lower() not in ["/login", "/player/login", "/register"]:
            self.redirect("/login")
            return

    def get_current_user(self):
        return SharedData().get_online_player(self.session_id)


class StreamingRequestHandler(BaseRequestHandler):
    def __init__(self, app, request, **kwargs):
        super().__init__(app, request, **kwargs)
        self.future = Future()
        self.alive = True

    def on_connection_close(self) -> None:
        self.alive = False

    def on_finish(self) -> None:
        self.alive = False
