import tornado.escape
import tornado.web

from SharedData import SharedData
from Model.Actions.BunkerEvents import RefreshRecruitsEvent
from Model.BaseClasses.BaseAction import ActionStatus
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler

from tornado import gen


class BunkerGetRecruits(BaseRequestHandler):
    def get(self):
        self.write(self.current_user.Organization.Bases[0].toJSON().encode())
        pass


class BunkerGetInfo(BaseRequestHandler):
    def post(self):
        bunker_id = tornado.escape.json_decode(self.request.body)["bunker_id"]
        b = SharedData().get_base(bunker_id)
        if not b.refresh_event or b.refresh_event.status == ActionStatus.FINISHED:
            b.refresh_event = RefreshRecruitsEvent(b.clear_recruits)
            SharedData().add_action(b.refresh_event)
            b.refresh_recruits()

        self.write(b.toJSON().encode())
        pass


class BunkerRecruitSoldier(BaseRequestHandler):
    def post(self):
        soldier_id = tornado.escape.json_decode(self.request.body)["recruit_id"]
        bunker_id = tornado.escape.json_decode(self.request.body)["bunker_id"]
        b = SharedData().get_base(bunker_id)
        soldier = [soldier for soldier in b.avail_recruits if soldier.id == soldier_id]

        if soldier:
            b.avail_recruits.remove(soldier[0])
            self.current_user.Crew.append(soldier[0])
            self.set_status(200)
        else:
            self.set_status(404)

        self.write(self.current_user.toJSON().encode())
        pass
