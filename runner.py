from FrontServer import FrontWatchServer
from BackServer import BackBoneServer
import asyncio
import SharedData

if asyncio.WindowsSelectorEventLoopPolicy:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    try:
        bbs = BackBoneServer()
        bbs.start()
        fws = FrontWatchServer()
        fws.run()
    except KeyboardInterrupt:
        print('Goodbye.')
#        bbs.stop()
