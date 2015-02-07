from pprint import pprint
from pysnap import Snapchat

import threading
import time

class GameInstance (threading.Thread):
    def __init__(self, organizer, gamePlayers):
        threading.Thread.__init__(self)
        self.api = Snapchat()
        self.api.login('snapsvshumanity', 'ilovetosnap69')

        self.players = []
        self.seensnaps = {}
        self.players.append({
                            'username': organizer,
                            'organizer': True,
                            'confirmed': False
                        })

        for p in gamePlayers.split():
            currentPlayer = {
                            'username': p,
                            'organizer': False,
                            'confirmed': False
                    }
            self.players.append(currentPlayer)

    def run(self):
        self.friendPlayers()
        self.sendGamePrompt()
        self.enterGameLoop()

    def sendGamePrompt(self):
        pass

    def enterGameLoop(self):
        pass

    def friendPlayers(self):
        friendslist = map(lambda x: x['name'], self.api.get_friends())
        toadd = list(set(map(lambda x: x['username'], self.players))
                - set(friendslist))
        for user in toadd:
            self.api.add_friend(user)
        #    self.sendInvitationSnap(user);

        unconfirmedPlayers = filter(lambda x: x['confirmed'] == False, self.players);

        while (len(unconfirmedPlayers) != 0):
            self.updateConfirmed(unconfirmedPlayers)
            unconfirmedPlayers = filter(lambda x: x['confirmed'] == False, self.players);
            time.sleep(60)


    def updateConfirmed(self, unconfirmedPlayers):
        snaps = set(self.api.get_snaps())
        unconfirmed = set(unconfirmedPlayers)
        for snap in snaps - self.seensnaps:
            if snap['sender'] in unconfirmed:
                fetchPhotoSnap(snap['id'], snap['id'])
                    # SPIN UP OCR THREAD HERE
                    # OCR STUFF(snaps/id)
                self.seensnaps.add(snap)



    def printPlayers(self):
        for p in self.players:
            print p['username']

    def listSnaps(self):
        snaps = [x for x in s.get_snaps() if x['status'] == 1]
        pprint(snaps)

    def fetchPhotoSnap(self, snapid, name):
        name = "snaps/" + snapid + ".jpg"
        f = open(name, 'wb')
        blob = self.api.get_blob(snapid)
        if blob == None:
            print "Snap not found!"
        else:
            f.write(blob)
        f.close()

    def sendSnap(self, path, recipients, time=5):
        mediaid = self.api.upload(path)
        self.api.send(mediaid, recipients, time)
