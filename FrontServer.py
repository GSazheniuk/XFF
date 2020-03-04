import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
from tornado import gen

from RequestHandlers import ChatHandlers, MapHandlers, PlayerHandlers, BunkerHandlers, BattleHandlers
from Model.Actions import GeoTimeAction, SpawnEvents

import Waiters
import SharedData


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("sessionId"):
            self.render("html\login.html")
        else:
            self.render("html\player_page.html", messages=[])


class ViewPlayerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\player_page.html", messages=[])


class ViewMapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\geoscape.html", messages=[])


class ViewBunkerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\\bunker.html", messages=[])


class ZKillTestHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_CHAT_MESSAGES)
        while not self.request.connection.stream.closed():
            kill = yield self.future
            print(kill)
            self.write(kill)
            self.flush()


class FrontWatchServer:
    
    def __init__(self):
        self.app = tornado.web.Application(
                [
                    (r"/", RootHandler),
                    (r"/map_view", ViewMapHandler),
                    (r"/base_view", ViewBunkerHandler),
                    (r"/player_view", ViewPlayerHandler),
                    (r"/player/login", PlayerHandlers.PlayerLoginPlayer),
                    (r"/player/getData", PlayerHandlers.PlayerGetData),
                    (r"/player/addSkill", PlayerHandlers.PlayerAddSkill2Queue),
                    # Map requests
                    (r"/map/getObjects", MapHandlers.MapGetObjects),
                    (r"/map/time", MapHandlers.MapTimer),
                    (r"/map/objects/([0-9]+)", MapHandlers.ObjectById),
                    (r"/map/all-objects", MapHandlers.MapAllObjects),
                    (r"/map/approachObject", MapHandlers.ApproachObject),
                    # Bunker requests
                    (r"/bunker/getData", BunkerHandlers.BunkerGetInfo),
                    (r"/bunker/recruitSoldier", BunkerHandlers.BunkerRecruitSoldier),
                    # Battle requests
                    (r"/attack_site", BattleHandlers.StartBattleHandler),
                    (r"/battle", BattleHandlers.BattleHandler),
                    # Chat requests
                    (r"/chat/getPlayers", ChatHandlers.ChatGetPlayers),
                    (r"/chat/getMessages", ChatHandlers.ChatGetMessages),
                    (r"/chat/gotMessages", ChatHandlers.ChatGotMessages),
                    (r"/chat/sendMessage", ChatHandlers.ChatSendMessage),
                    # test stuff
                    (r"/zkill", ZKillTestHandler),
                    # Static resources handlers
                    (r"/themes/(.*)", tornado.web.StaticFileHandler, {"path": "static\\themes\\"}),
                    (r"/data/(.*)", tornado.web.StaticFileHandler, {"path": "static\\Data\\"}),
                    (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': 'static\\js\\'}),
                    (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "static\\images\\"}),
                    ],
                cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                template_path=os.path.join(os.path.dirname(__file__), "static"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
                debug=True,
            )
        pass

    def run(self):
        self.app.listen(8081)
        SharedData.Loop.actions.append(GeoTimeAction.TimeAction())
        SharedData.Loop.actions.append(SpawnEvents.SpawnSiteEvent())
        tornado.ioloop.IOLoop.current().add_callback(SharedData.Loop.start_loop)
        tornado.ioloop.IOLoop.current().start()
        pass
