import tornado.escape
import tornado.web

from tornado import gen
from SharedData import SharedData
from Waiters import AWaiters
from Model.BaseClasses.BaseRequest import BaseRequestHandler, StreamingRequestHandler


class ChatGetPlayers(StreamingRequestHandler):
    @gen.coroutine
    def post(self):
        print(self.request.body)
        channel = tornado.escape.json_decode(self.request.body)["channel"]
        refresh_all = tornado.escape.json_decode(self.request.body)["refresh_all"]
        if refresh_all != 1:
            self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_CHAT_PLAYERS)
            yield self.future
            if not self.alive:
                return

        players = SharedData().get_players_on_channel(channel)
        res = '{ "players" : ['
        for token_id in players:
            player = SharedData().get_player_by_token(token_id)
            res += ',{"name": "%s"}' % player.Name
            pass
        res += "]}"
        self.write(res.replace("[,", "["))
        pass


class ChatSendMessage(BaseRequestHandler):
    def post(self):
        print(self.request.body)
        post_data = tornado.escape.json_decode(self.request.body)
        channel = post_data["channel"]
        message = post_data["message"]
        r = SharedData().send_message(self.current_user, channel, message)
        AWaiters().deliver(AWaiters.WAIT_FOR_CHAT_MESSAGES, r)
        self.write("{}")
        pass


class ChatGetMessages(StreamingRequestHandler):
    @gen.coroutine
    def post(self):
        self.future = AWaiters().subscribe(AWaiters.WAIT_FOR_CHAT_MESSAGES)
        msgs = yield self.future

        if not self.alive:
            return

        print(msgs)

        res = '{ "result": ['
        for channel in msgs:
            res += ', {"channel" : "%s", "messages" : [' % channel
            print(msgs[channel])
            for message in msgs[channel]:
                print(message)
                res += ', {"message" : ["%s", "%s", "%s"]}' % message
                pass
            res += "]}"
            pass
        res += "]}"
        res = res.replace("[,", "[")
        print(res)
        self.write(res)
        pass


class ChatGotMessages(BaseRequestHandler):
    def post(self):
        # player = SharedData.get_current_player(self)
        self.write("{}")
        pass
