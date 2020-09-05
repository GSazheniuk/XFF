import tornado.escape
import tornado.web

from SharedData import SharedData
from Waiters import AWaiters
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler
from tornado import gen


class StartBattleHandler(BaseRequestHandler):
    def __init__(self, app, request, **kwargs):
        super().__init__(app, request, **kwargs)
        try:
            site_id = self.get_cookie("site_id")
            self.site = SharedData().get_combat_site(int(site_id))
        except:
            self.site = None

    def get(self):
        self.render("html/battle.html", player_team=self.current_user.Crew, enemy_team=self.site.Crew)

    def post(self):
        site_id = tornado.escape.json_decode(self.request.body)["site_id"]
        self.set_cookie("site_id", site_id)
        self.site = SharedData().get_combat_site(int(site_id))
        self.site.start_battle(self.current_user)
        self.write(b'{}')


class BattleHandler(StreamingRequestHandler):
    @gen.coroutine
    def get(self):
        rep = ""
        while self.alive and rep != "Done.":
            self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_BATTLE_EVENTS)
            rep = yield self.future
            if not self.alive:
                return
            self.write(rep)
            self.flush()
