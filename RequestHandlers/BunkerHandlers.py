import tornado.escape
import tornado.web

import SharedData
from Model.Actions.BunkerEvents import RefreshRecruitsEvent
from Model.BaseClasses.BaseAction import ActionStatus
import Waiters

from tornado import gen


class BunkerGetRecruits(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        player = SharedData.get_current_player(self)

        self.write(player.Organization.Bases[0].toJSON().encode())
        pass

    def on_connection_close(self):
        pass


class BunkerGetInfo(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        player = SharedData.get_current_player(self)
        if not player:
            pass

        bunker_id = tornado.escape.json_decode(self.request.body)["bunker_id"]
        b = SharedData.AllBases[bunker_id]
        if not b.refresh_event or b.refresh_event.status == ActionStatus.FINISHED:
            b.refresh_event = RefreshRecruitsEvent(b.clear_recruits)
            SharedData.Loop.actions.append(b.refresh_event)
            b.refresh_recruits()

        self.write(b.toJSON().encode())
        pass

    def on_connection_close(self):
        pass


class BunkerRecruitSoldier(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        player = SharedData.get_current_player(self)
        if not player:
            pass

        soldier_id = tornado.escape.json_decode(self.request.body)["recruit_id"]
        bunker_id = tornado.escape.json_decode(self.request.body)["bunker_id"]
        b = SharedData.AllBases[bunker_id]
        soldier = [soldier for soldier in b.avail_recruits if soldier.id == soldier_id]

        if soldier:
            b.avail_recruits.remove(soldier[0])
            player.Crew.append(soldier[0])
            self.set_status(200)
        else:
            self.set_status(404)

        self.write(player.toJSON().encode())
        pass

    def on_connection_close(self):
        pass
