import uuid
from Model.BaseClasses.BaseObjects import BaseObject
from SharedData import SharedData


class Organization(BaseObject):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ""
        self.bio = ""
        self.leader_id = 0
        self.is_NPC = False
        self.hq_id = None

    def new(self, name, descr, leader_id, is_npc, hq_id=None):
        self.name = name
        self.hq_id = hq_id
        self.bio = descr
        self.leader_id = leader_id
        self.is_NPC = is_npc

    def save(self):
        SharedData().save_organization(o=self)
