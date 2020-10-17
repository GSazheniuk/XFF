from FrontServer import FrontWatchServer
from BackServer import BackBoneServer

from SharedData import SharedData
import OrganizationClass, PlayerClass
from Tools import MainLoader

MainLoader.load_all()

try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    pass


if __name__ == '__main__':
    try:
        # bbs = BackBoneServer()
        # bbs.start()
        fws = FrontWatchServer()
        fws.run()
    except KeyboardInterrupt:
        print('Goodbye.')
#        bbs.stop()
