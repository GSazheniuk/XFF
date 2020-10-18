from Model.Havens.Headquarters import Headquarters
from OrganizationClass import Organization
from PlayerClass import NPCCharacter
from SharedData import SharedData


def load_all():
    SharedData()
    load_npcs()
    load_havens()
    load_organizations()


def load_havens():
    print("Loading Havens...", end="")
    for o in SharedData().mongo_helper.Havens.find():
        haven = eval(o["type"])()
        haven.load_from_JSON(o)
        SharedData().havens[haven.id] = haven
        SharedData().add_base(haven)
    print("OK")


def load_organizations():
    print("Loading Organizations...", end="")
    for o in SharedData().mongo_helper.organizations.find():
        org = Organization()
        org.load_from_JSON(o)
        SharedData().organizations[org.id] = org
    print("OK")


def load_npcs():
    print("Loading NPCs...", end="")
    for o in SharedData().mongo_helper.NPCs.find():
        npc = NPCCharacter()
        npc.load_from_JSON(o)
        SharedData().NPCs[npc.id] = npc
    print("OK")
