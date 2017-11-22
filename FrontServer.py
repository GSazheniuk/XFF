import tornado.escape
import tornado.ioloop
import tornado.web
import os.path

import ChatHandlers
import MapHandlers
import PlayerHandlers


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\player_page.html", messages=[])


class ViewPlayerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\player_page.html", messages=[])


class ViewMapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html\home.html", messages=[])


class FrontWatchServer:
    
    def __init__(self):
        self.app = tornado.web.Application(
                [
                    (r"/", RootHandler),
                    (r"/map_view", ViewMapHandler),
                    (r"/player_view", ViewPlayerHandler),
                    (r"/player/login", PlayerHandlers.PlayerLoginPlayer),
                    (r"/player/getData", PlayerHandlers.PlayerGetData),
                    (r"/player/addSkill", PlayerHandlers.PlayerAddSkill2Queue),
                    # Map requests
                    (r"/map/getObjects", MapHandlers.MapGetObjects),
                    (r"/map/approachObject", MapHandlers.ApproachObject),
                    # Chat requests
                    (r"/chat/getPlayers", ChatHandlers.ChatGetPlayers),
                    (r"/chat/getMessages", ChatHandlers.ChatGetMessages),
                    (r"/chat/gotMessages", ChatHandlers.ChatGotMessages),
                    (r"/chat/sendMessage", ChatHandlers.ChatSendMessage),
                    # Static resources handlers
                    (r"/themes/(.*)", tornado.web.StaticFileHandler, {"path": "static\\themes\\"}),
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
        tornado.ioloop.IOLoop.current().start()
        pass
