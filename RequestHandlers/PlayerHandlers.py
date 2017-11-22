import tornado.web
import tornado.escape
import random

import Waiters
import config
import SharedData

from NPCOrganizationsHelper import NPCOrganizations
from PlayerClass import Player


class PlayerGetData(tornado.web.RequestHandler):
    def initialize(self):
        self.sessionId = self.get_cookie("sessionId")
        pass

    def get(self):
        if self.sessionId in SharedData.OnlinePlayers:
            cp = SharedData.Players[SharedData.OnlinePlayers[self.sessionId]]
            self.write(cp.toJSON().encode())
        else:
            self.write(b"{}")
        pass


class PlayerLoginPlayer(tornado.web.RequestHandler):
    def initialize(self):
        self.sessionId = self.get_cookie("sessionId")
        if self.sessionId is None:
            self.sessionId = str(random.randint(config.PLAYER_MIN_ID, config.PLAYER_MAX_ID))
            self.set_cookie("sessionId", self.sessionId)
        pass

    def get(self):
        if (self.sessionId is not None) and (self.sessionId in SharedData.OnlinePlayers):
            self.redirect("/")
        else:
            self.render("html\login.html")
        pass

    def post(self):
        npc_org = NPCOrganizations()
        player = Player(
            "Vincent"
            , "Merle"
            , npc_org.get_random_org()
            , random.randint(1000000, 10000000)
            , SharedData.Map.DefaultSector
        )

        SharedData.OnlinePlayers[self.sessionId] = player.Token
        SharedData.Players[player.Token] = player

        SharedData.Chat.subscribe_player_to_channel(player, "local")
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_CHAT_PLAYERS, player)

        player.CurrentSector.add_object(player.MapObject)

        self.redirect("/")
        pass


class PlayerAddSkill2Queue(tornado.web.RequestHandler):
    def post(self):
        session_id = self.get_cookie("sessionId")
        post_data = tornado.escape.json_decode(self.request.body)
        skill_name = post_data["skill_name"]

        if session_id in SharedData.OnlinePlayers:
            cp = SharedData.Players[SharedData.OnlinePlayers[session_id]]
            cp.add_skill_to_queue(skill_name)
            pass

        self.write(b"{}")
        pass
