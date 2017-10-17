import tornado.escape
import tornado.web

from tornado import gen

from SharedData import DataHolder


class MapGetObjects(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        player = DataHolder.get_current_player(self.get_cookie("tokenId"))
#        post_data = tornado.escape.json_decode(self.request.body)
#        channel = post_data["channel"]

        self.future = player.CurrentSector.get_objects_on_map()
        objects = yield self.future

        if self.request.connection.stream.closed():
            return

        print(objects)

        self.write(str(objects))
        pass

    def on_connection_close(self):
        player = DataHolder.get_current_player(self.get_cookie("tokenId"))
        player.CurrentSector.cancel_wait(self.future)
        pass
