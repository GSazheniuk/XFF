from FrontServer import FrontWatchServer
from BackServer import BackBoneServer

try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    pass

import SharedData


if __name__ == '__main__':
    try:
        bbs = BackBoneServer()
        bbs.start()
        fws = FrontWatchServer()
        fws.run()
    except KeyboardInterrupt:
        print('Goodbye.')
#        bbs.stop()
