from Model.Havens.Headquarters import Headquarters
from OrganizationClass import Organization
from SharedData import SharedData


def load_all():
    SharedData()
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
