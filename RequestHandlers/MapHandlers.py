import tornado.escape
import tornado.web

import SharedData
import Waiters

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

        objects = player.CurrentSector.get_objects_on_map_json()
        # self.write(tornado.escape.json_encode(objects))
        self.write(objects.encode())
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


class ObjectById(tornado.web.RequestHandler):
    def get(self, objectId, *args, **kwargs):
        oId = int(objectId)
        if oId in SharedData.Map.DefaultSector.objects:
            self.set_status(200)
            self.write(SharedData.Map.DefaultSector.objects[oId].toJSON())
        else:
            self.set_status(404)
            print(SharedData.Map.DefaultSector.objects)
            self.write("{}")
        pass


class MapAllObjects(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        objects = SharedData.Map.DefaultSector.get_objects_on_map_json()
        self.set_status(200)
        self.write(objects)
    pass


class MapTimer(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        ctime = SharedData.Loop.actions[0].current_time
        self.write(ctime.strftime("%Y-%b-%d %H:%M:%S").encode())
        return
#        while not self.request.connection.stream.closed():
#            self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_TIMER)
#            ctime = yield self.future
#            if not self.request.connection.stream.closed():
#                self.write(ctime.strftime("%Y-%b-%d %H:%M:%S").encode())
#                self.flush()
        pass

    def on_connection_close(self):
#        Waiters.all_waiters.cancel_waiter(Waiters.WAIT_FOR_TIMER, self.future)
        pass
