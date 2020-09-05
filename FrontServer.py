import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
from tornado import gen
from tornado.concurrent import Future

from RequestHandlers import ChatHandlers, MapHandlers, PlayerHandlers, BunkerHandlers, BattleHandlers
from Model.Actions import GeoTimeAction, SpawnEvents
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler

from Waiters import AWaiters
from SharedData import SharedData


class RootHandler(BaseRequestHandler):
    def get(self):
        self.render("html/player_page.html")


class LoginHandler(BaseRequestHandler):
    def get(self):
        self.render("html/login.html")


class ViewMapHandler(BaseRequestHandler):
    def get(self):
        self.render("html/geoscape.html")


class ViewBunkerHandler(BaseRequestHandler):
    def get(self):
        self.render("html/bunker.html")


class ZKillTestHandler(StreamingRequestHandler):
    @gen.coroutine
    def get(self):
        self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_CHAT_MESSAGES)
        while self.alive:
            kill = yield self.future
            print(kill)
            self.write(kill)
            self.flush()


class FrontWatchServer:
    def __init__(self):
        self.app = tornado.web.Application(
            [
                (r"/", RootHandler),
                (r"/login", LoginHandler),
                (r"/map_view", ViewMapHandler),
                (r"/base_view", ViewBunkerHandler),
                (r"/player_view", RootHandler),
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
                (r"/themes/(.*)", tornado.web.StaticFileHandler, {"path": "static/themes/"}),
                (r"/data/(.*)", tornado.web.StaticFileHandler, {"path": "static/Data/"}),
                (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': 'static/js/'}),
                (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "static/images/"}),
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
        SharedData().add_action(GeoTimeAction.TimeAction())
        SharedData().add_action(SpawnEvents.SpawnSiteEvent())
        tornado.ioloop.IOLoop.current().add_callback(SharedData().start_loop)
        tornado.ioloop.IOLoop.current().start()
        pass
