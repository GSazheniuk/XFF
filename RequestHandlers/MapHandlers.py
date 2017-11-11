import tornado.escape
import tornado.web

import SharedData
import Waiters
import config

from tornado import gen


class MapGetObjects(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        player = SharedData.get_current_player(self)
        refresh_all = tornado.escape.json_decode(self.request.body)["refresh_all"]

#        post_data = tornado.escape.json_decode(self.request.body)
#        channel = post_data["channel"]

        if refresh_all != 1:
            self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_MAP_OBJECTS)
            yield self.future
            if self.request.connection.stream.closed():
                return
            pass

        if self.request.connection.stream.closed():
            return

        objects = player.CurrentSector.get_objects_on_map()
        print(objects)
        self.write(tornado.escape.json_encode(objects))
        pass

    def on_connection_close(self):
        Waiters.all_waiters.cancel_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, self.future)
        pass


class ApproachObject(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        player = SharedData.get_current_player(self)
        object_id = tornado.escape.json_decode(self.request.body)["object_id"]
        # SharedData.add_map_action(player, object_id, config.MapActionTypes.ACTION_TYPE_APPROACH)
        self.write("{}")
        pass
