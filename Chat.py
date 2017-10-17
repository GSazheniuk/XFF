class Chat:
    def __init__(self):
        self.Channels = []
        self.Channels2Players = {}
        self.Players2Channels = {}
        self.PlayerMessages = {}
        pass

    def new_channel(self, channel):
        self.Channels.append(channel)
        pass

    def subscribe_player_to_channel(self, player, channel):
        if channel not in self.Channels:
            self.new_channel(channel)
            pass

        if channel not in self.Channels2Players:
            self.Channels2Players[channel] = []
            pass

        if player.Token not in self.Players2Channels:
            self.Players2Channels[player.Token] = []
            pass

        if player.Token not in self.PlayerMessages:
            self.PlayerMessages[player.Token] = {}
            pass

        if channel not in self.PlayerMessages[player.Token]:
            self.PlayerMessages[player.Token][channel] = []
            pass

        self.Channels2Players[channel].append(player.Token)
        self.Players2Channels[player.Token].append(channel)
        pass
    
    def unsubscribe_player_from_channel(self, player, channel):
        self.Channels2Players[channel].remove(player.Token)
        self.Players2Channels[player.Token].remove(channel)
        del self.PlayerMessages[player.Token][channel]
        pass
    
    def send_message(self, player, channel, message):
        if channel not in self.Channels:
            self.new_channel(channel)
            print('Channel created')
            self.subscribe_player_to_channel(player, channel)
            print('Player subscribed')
            pass
        
        print('Message sent 1')
        for p in self.Channels2Players[channel]:
            self.PlayerMessages[p][channel].append((player.Token, player.Name, message))
            pass

        res = {}
        res[channel] = [(player.Token, player.Name, message)]
        return res

    def get_messages(self, player):
        res = {}
        for channel in self.PlayerMessages[player.Token]:
            res[channel] = []
            for message in self.PlayerMessages[player.Token][channel]:
                res[channel].append(message)
                pass
            pass
        pass
        return res

    def clean_messages(self, player):
        for channel in self.PlayerMessages[player.Token]:
            del self.PlayerMessages[player.Token][channel][:]
            pass
        pass
