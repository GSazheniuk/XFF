import tornado.escape
import tornado.web

import Waiters
import SharedData

from tornado import gen


class ChatGetPlayers(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print(self.request.body)
        channel = tornado.escape.json_decode(self.request.body)["channel"]
        refresh_all = tornado.escape.json_decode(self.request.body)["refresh_all"]
        if refresh_all != 1:
            self.future = Waiters.all_waiters.subscribe_waiter(Waiters.WAIT_FOR_CHAT_PLAYERS)
            yield self.future
            if self.request.connection.stream.closed():
                return
            pass

        players = SharedData.Chat.Channels2Players[channel]
        res = '{ "players" : ['
        for TokenId in players:
            player = SharedData.Players[TokenId]
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
        player = SharedData.get_current_player(self)
        r = SharedData.Chat.send_message(player, channel, message)
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
        # player = SharedData.get_current_player(self)
        self.write("{}")
        pass
