import tornado.escape
import tornado.web

from SharedData import SharedData
from Waiters import AWaiters
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler

from tornado import gen


class MapGetObjects(StreamingRequestHandler):
    @gen.coroutine
    def post(self):
        refresh_all = tornado.escape.json_decode(self.request.body)["refresh_all"]

        if refresh_all != 1:
            self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_MAP_OBJECTS)
            yield self.future

        if not self.alive:
            return

        objects = self.current_user.CurrentSector.get_objects_on_map_json()
        self.write(objects)
        pass


class ApproachObject(BaseRequestHandler):
    def post(self, *args, **kwargs):
        object_id = tornado.escape.json_decode(self.request.body)["object_id"]
        # SharedData.add_map_action(player, object_id, config.MapActionTypes.ACTION_TYPE_APPROACH)
        self.write("{}")
        pass


class ObjectById(BaseRequestHandler):
    def get(self, objectId):
        map_obj = SharedData().get_map_object_by_id(int(objectId))
        if map_obj:
            self.set_status(200)
            self.write(map_obj.dict())
        else:
            self.set_status(404)
            self.write("{}")
        pass


class MapAllObjects(tornado.web.RequestHandler):
    def get(self):
        objects = SharedData().get_all_map_objects_json()
        self.set_status(200)
        self.write(objects)
    pass


class MapTimer(StreamingRequestHandler):
    @gen.coroutine
    def get(self):
        while self.alive:
            self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_TIMER)
            ctime = yield self.future
            if self.alive:
                self.write(ctime.encode())
                self.flush()
