import tornado.escape
import tornado.web

import SharedData
from Model.Actions.BunkerEvents import RefreshRecruitsEvent
from Model.BaseClasses.BaseAction import ActionStatus
import Waiters

from tornado import gen


class StartBattleHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("html/battle.html", messages=[])

    def post(self):
        player = SharedData.get_current_player(self)
        if not player:
            pass

        site_id = int(tornado.escape.json_decode(self.request.body)["site_id"])
        site = SharedData.AllFlyingObjects[site_id]
        site.start_battle(player)
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
