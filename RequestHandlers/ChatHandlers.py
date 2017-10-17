import tornado.escape
import tornado.web

import Waiters

from tornado import gen
from SharedData import DataHolder


class ChatGetPlayers(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_CHAT_PLAYERS)
        msgs = yield self.future

        if self.request.connection.stream.closed():
            return

        print(msgs)
        print(self.request.body)
        channel = tornado.escape.json_decode(self.request.body)["channel"]
        players = DataHolder.Chat.Channels2Players[channel]
        res = '{ "players" : ['
        for TokenId in players:
            player = DataHolder.Players[TokenId]
            res += ',{"name": "%s"}' % player.Name
            pass
        res += "]}"
        self.write(res.replace("[,", "["))
        pass

    def on_connection_close(self):
        Waiters.all_waiters.cancel_waiter(Waiters.WAIT_FOR_CHAT_PLAYERS, self.future)
        pass


class ChatSendMessage(tornado.web.RequestHandler):
    def post(self):
        print(self.request.body)
        post_data = tornado.escape.json_decode(self.request.body)
        channel = post_data["channel"]
        message = post_data["message"]
        player = DataHolder.get_current_player(self.get_cookie("tokenId"))
        r = DataHolder.Chat.send_message(player, channel, message)
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_CHAT_MESSAGES, r)
        self.write("{}")
        pass


class ChatGetMessages(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_CHAT_MESSAGES)
        msgs = yield self.future

        if self.request.connection.stream.closed():
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

    def on_connection_close(self):
        Waiters.all_waiters.cancel_waiter(Waiters.WAIT_FOR_CHAT_MESSAGES, self.future)
        pass


class ChatGotMessages(tornado.web.RequestHandler):
    def post(self):
        player = DataHolder.get_current_player(self.get_cookie("tokenId"))
        self.write("{}")
        pass
