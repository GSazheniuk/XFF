import tornado.web
import random

import Waiters

from SharedData import DataHolder
from NPCOrganizationsHelper import NPCOrganizations
from PlayerClass import Player


class PlayerGetData(tornado.web.RequestHandler):
    def initialize(self):
        self.tokenId = self.get_cookie("tokenId")
        print(self.tokenId)
        pass

    def get(self):
        print('PlayerGetData: ', self.tokenId)
        print('OnlinePlayers: ', DataHolder.OnlinePlayers)
        if self.tokenId in DataHolder.OnlinePlayers:
            cp = DataHolder.Players[DataHolder.OnlinePlayers[self.tokenId]]
            self.write(cp.toJSON().encode())
            pass
        else:
            self.write(b"{}")
        pass


class PlayerLoginPlayer(tornado.web.RequestHandler):
    def initialize(self):
        self.tokenId = self.get_cookie("tokenId")
        pass

    def get(self):
        if self.tokenId:
            self.redirect("/")
        else:
            self.render("html\login.html", messages=[])
        pass

    def post(self):
        npc_org = NPCOrganizations()
        player = Player(
            "Vincent"
            , "Merle"
            , npc_org.get_random_org()
            , random.randint(1000000, 10000000)
            , DataHolder.Map.DefaultSector
        )

        DataHolder.OnlinePlayers[self.tokenId] = player.Token
        DataHolder.Players[player.Token] = player

        DataHolder.Chat.subscribe_player_to_channel(player, "local")
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_CHAT_PLAYERS, player)

        self.redirect("/")
        pass
