import uuid
from Model.BaseClasses.BaseObjects import BaseObject
from SharedData import SharedData


class Organization(BaseObject):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.Name = ""
        self.Bio = ""
        self._leader_id = 0
        self.NPC = False

    def new(self, name, descr, leader_id, is_npc):
        self.id = uuid.uuid4().hex
        self.Name = name
        self.Bio = descr
        self._leader_id = leader_id
        self.NPC = is_npc

    def save(self):
        SharedData().save_organization(o=self)
