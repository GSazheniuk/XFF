import tornado.escape
import tornado.web

import SharedData
from Model.Actions.BunkerEvents import RefreshRecruitsEvent
from Model.BaseClasses.BaseAction import ActionStatus
import Waiters

from tornado import gen


class StartBattleHandler(tornado.web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super().__init__(app, request, **kwargs)
        try:
            site_id = self.get_cookie("site_id")
            self.site = SharedData.AllFlyingObjects[int(site_id)]
        except:
            self.site = None

    @gen.coroutine
    def get(self):
        player = SharedData.get_current_player(self)
        self.render("html/battle.html", player_team=player.Crew, enemy_team=self.site.Crew, messages=[])

    def post(self):
        player = SharedData.get_current_player(self)
        if not player:
            pass

        site_id = tornado.escape.json_decode(self.request.body)["site_id"]
        self.set_cookie("site_id", site_id)
        self.site = SharedData.AllFlyingObjects[int(site_id)]
        self.site.start_battle(player)
        self.write(b'{}')


class BattleHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        rep = ""
        while not self.request.connection.stream.closed() and rep != "Done.":
            self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_BATTLE_EVENTS)
            rep = yield self.future
            self.write(rep)
            self.flush()
