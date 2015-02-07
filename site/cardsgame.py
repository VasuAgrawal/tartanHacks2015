from pprint import pprint
from pysnap import Snapchat

class GameInstance:
    def __init__(self, gamePlayers):
        self.api = Snapchat()
        self.api.login('snapsvshumanity', 'ilovetosnap69')

        self.players = []
        for p in gamePlayers:
            currentPlayer = {}
            currentPlayer['username'] = p
            self.players.append(currentPlayer)

    def printPlayers(self):
        for p in self.players:
            print p['username']

    def listSnaps(self):
        snaps = [x for x in s.get_snaps() if x['status'] == 1]
        pprint(snaps)

    def fetchPhotoSnap(self, snapid, name):
        name = "snaps/" + snapid + ".jpg"
        with f as open(name, 'wb'):
            blob = self.api.get_blob(snapid)
            if blob == None:
                print "Snap not found!"
            else:
                f.write(blob)
                f.close()

    def sendSnap(self, path, recipients, time=5):
        mediaid = self.api.upload(path)
        self.api.send(mediaid, recipients, time)
