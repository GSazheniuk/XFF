from Model.MongoCollections import UFOs, GroundSite
from Logger import Logger
from Chat import Chat
from map import Map
from Geoscape.GeoLoop import GeoLoop
from Tools import mongohelper
from Model.BaseClasses.Singleton import Singleton

import config
import random


class SharedData(metaclass=Singleton):
    def __init__(self):
        print("Shared Data initializing....")
        self._online = {}
        self._players = {}
        self._all_ufos = {}
        self._all_bases = {}
        self._sessions = {}
        self._chat = Chat()
        self._map = Map(1, 1)
        self._log = Logger('XFF', 'SharedData')
        self._map_actions = {}
        self._skill_queues = []
        self._loop = GeoLoop()

        self._mongo_helper = mongohelper.MongoHelper()
        # Populate UFOs collection with default objects
        if config.BACKSERVER_POPULATE_MONGO:
            self._mongo_helper.add_ufo(UFOs.Probe())
            self._mongo_helper.add_ufo(UFOs.SmallScout())
            self._mongo_helper.add_ufo(UFOs.MediumScout())
            self._mongo_helper.add_ufo(UFOs.LargeScout())
            self._mongo_helper.add_site(GroundSite.BasicSectoidOperation())

        # Load Collections from Mongo
        self._ufos = self._mongo_helper.get_all_ufos()
        self._sites = self._mongo_helper.get_all_sites()

        print("Shared Data initialized OK....")

    def is_online(self, session_id):
        return session_id in self._online

    def add_online(self, session_id):
        if session_id not in self._online:
            self._online[session_id] = None

    def get_online(self, session_id):
        if session_id not in self._online:
            return None
        else:
            return self._online[session_id]

    def add_action(self, action):
        self._loop.actions.append(action)

    def start_loop(self):
        self._loop.start_loop()

    def add_base(self, b):
        self._all_bases[b.get_id()] = b

    def get_default_sector(self):
        return self._map.DefaultSector

    def remove_ufo(self, ufo_id):
        del self._all_ufos[ufo_id]

    def get_online_player(self, session_id):
        if self.is_online(session_id) and self._online[session_id]:
            return self._players[self._online[session_id]]
        return None

    def add_online_player(self, session_id, player):
        self._online[session_id] = player.Token
        self._players[player.Token] = player
        self._chat.subscribe_player_to_channel(player, "local")

    def get_map_object_by_id(self, object_id):
        if object_id in self._map.DefaultSector.objects:
            return self._map.DefaultSector.objects[object_id]
        else:
            return None

    def get_all_map_objects_json(self):
        return self._map.DefaultSector.get_objects_on_map_json()

    def get_players_on_channel(self, channel):
        return self._chat.Channels2Players[channel]

    def get_player_by_token(self, token_id):
        if token_id in self._players:
            return self._players[token_id]
        else:
            return None

    def send_message(self, player, channel, message):
        self._chat.send_message(player, channel, message)

    def get_base(self, base_id):
        if base_id in self._all_bases:
            return self._all_bases[base_id]
        else:
            return None

    def get_combat_site(self, site_id):
        if site_id in self._all_ufos:
            return self._all_ufos[site_id]
        else:
            return None

    def spawn_combat_sites(self, site_constructor):
        probability = random.randint(0, config.EVENTS_MAX_PROBABILITY)
        sites = [e for e in self._sites if e['probability'] > probability]
        for u in sites:
            site = site_constructor(u, SharedData().get_default_sector())
            self._all_ufos[site.map_object.id] = site

    def save_organization(self, o):
        self._mongo_helper.save_organization(o)

    def save_npc_character(self, npc):
        self._mongo_helper.save_npc_character(npc)
