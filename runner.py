from FrontServer import FrontWatchServer
from BackServer import BackBoneServer

if __name__ == '__main__':
    try:
        bbs = BackBoneServer()
        bbs.start()
        fws = FrontWatchServer()
        fws.run()
    except KeyboardInterrupt:
        print('Goodbye.')
#        bbs.stop()
