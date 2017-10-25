import config

from pymongo import MongoClient, errors


class MongoHelper:
    def __init__(self):
        self._mClient = MongoClient(config.MONGO_CONNECTION_STRING)
        self._db = self._mClient['xcom']
        self.ufos = self._db.get_collection('UFOs')
        pass

    def add_ufo(self, o):
        self.ufos.find_one_and_replace({'_id': o.get_id()}, o.__dict__, upsert=True)
        pass

    def get_all_ufos(self):
        ufos = []
        try:
            for u in self.ufos.find():
                ufos.append(u)
        except errors.ServerSelectionTimeoutError:
            ufos.append({
                "_id": 0,
                "probability": 45000,
                "max_crew_level": 1,
                "diameter": 3,
                "ufo_type": "Probe",
                "max_structure": 100,
                "max_loot": 3,
                "bounty": 100,
                "max_armor": 100,
                "min_loot": 1,
                "min_crew": 1,
                "max_crew": 1,
                "duration": 25,
                "max_instances_in_sector": 10,
                "max_shields": 100,
                "max_speed": 100
            })
            pass
        return ufos
