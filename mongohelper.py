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
            pass
        return ufos
