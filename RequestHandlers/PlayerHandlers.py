import tornado.web
import tornado.escape
import random

import config
from SharedData import SharedData

from NPCOrganizationsHelper import NPCOrganizations
from PlayerClass import Player
from Waiters import AWaiters
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler


class PlayerGetData(BaseRequestHandler):
    def get(self):
        cp = SharedData().get_online_player(self.session_id)
        if cp:
            # self.write(cp.toJSON().replace(",}", "}").replace(",]", "]"))
            self.write(cp.dict())
        else:
            self.write(b"{}")
        pass


class PlayerLoginPlayer(BaseRequestHandler):
    def get(self):
        if SharedData().is_online(self.session_id):
            self.redirect("/")
        else:
            self.render("html/login.html")
        pass

    def post(self):
        npc_org = NPCOrganizations()
        player = Player(
            "Vincent"
            , "Merle"
            , SharedData().organizations[
                next((org for org in SharedData().organizations if SharedData().organizations[org].name == "X-COM"))
            ]
            , random.randint(1000000, 10000000)
            , SharedData().get_default_sector()
        )
        SharedData().add_online_player(self.session_id, player)
        AWaiters().deliver(AWaiters.WAIT_FOR_CHAT_PLAYERS, player)
    
        player.CurrentSector.add_object(player.MapObject)

        self.redirect("/")
        pass


class PlayerAddSkill2Queue(tornado.web.RequestHandler):
    def post(self):
        post_data = tornado.escape.json_decode(self.request.body)
        skill_name = post_data["skill_name"]

        self.current_user.add_skill_to_queue(skill_name)
        self.write(b"{}")
        pass
