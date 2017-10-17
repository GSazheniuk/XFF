from OrganizationClass import Organization
import random

class NPCOrganizations:
    def __init__(self):
        self.AllOrgs = []
        self.AllOrgs.append(Organization('Megapol'))
        self.AllOrgs.append(Organization('Cult of Sirius'))
        self.AllOrgs.append(Organization('Marsec'))
        self.AllOrgs.append(Organization('Transtellar'))
        self.AllOrgs.append(Organization('Solmine'))
        self.AllOrgs.append(Organization('Cyberweb'))
        self.AllOrgs.append(Organization('General Metro'))
        self.AllOrgs.append(Organization('Superdynamics'))
        self.AllOrgs.append(Organization('Diablo'))
        self.AllOrgs.append(Organization('Nanotech'))
        self.AllOrgs.append(Organization('Mutant Alliance'))
        self.AllOrgs.append(Organization('S.E.L.F.'))
        self.AllOrgs.append(Organization('Energen'))
        self.AllOrgs.append(Organization('Evonet'))
        self.AllOrgs.append(Organization('Extropians'))
        self.AllOrgs.append(Organization('Grav Ball League'))
        self.AllOrgs.append(Organization('Lifetree'))
        self.AllOrgs.append(Organization('Nutrivend'))
        self.AllOrgs.append(Organization('Osiron'))
        self.AllOrgs.append(Organization('Psyke'))
        self.AllOrgs.append(Organization('Sanctuary Clinic'))
        self.AllOrgs.append(Organization('Sensovision'))
        self.AllOrgs.append(Organization('Synthemesh'))
        self.AllOrgs.append(Organization('Technocrats'))
        self.AllOrgs.append(Organization('X-COM'))
        pass

    def get_random_org(self):
        return random.choice(self.AllOrgs)

    
