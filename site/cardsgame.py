from pprint import pprint
from pysnap import Snapchat
from ripText import TextDetector

import time

class RoundStage:
    Entries = 0
    Judging = 1

class GameInstance:
    players = []
    currentJudge = None

    api = None
    processedSnaps = []

    gameRound = 0
    roundStage = RoundStage.Entries
    roundStart = 0
    roundDuration = 60 * 5  # i.e. five minutes
    numCycles = 1
    gameFinished = False

    # Constructor
    def __init__(self, organizer, gamePlayers):
        self.api = Snapchat()
        self.api.login('snapsvshumanity', 'ilovetosnap69')

        gameround = 0;

        self.players.append({
                            'username' : organizer,
                            'organizer': True,
                            'confirmed': False,
                            'judged'   : False
                        })

        for p in gamePlayers.split():
            currentPlayer = {
                            'username' : p,
                            'organizer': False,
                            'confirmed': False,
                            'judged'   : False
                    }
            self.players.append(currentPlayer)

    # Main logic loop
    def run(self):
        self.friendPlayers()
        while (not gameFinished):
            snaps = self.pollAndFetchSnaps()
            self.processSnaps(snaps)

            if self.gameRound == 0:
                self.checkForAccepts()
            elif self.gameRound > self.numCycles * len(self.players):
                self.sendWinnerAndClose()
            elif self.roundStage == RoundStage.Entries:
                if (time.time() - self.roundStart > self.roundDuration):
                    self.roundStage = RoundStage.Judging
                    self.proceedToJudging()
            else:
                print "This shouldn't happen"
            time.sleep(30)

    # For each snap in snaps, OCR/classify
    def processSnaps(self, snaps):
        pass

    # Checks to see who won by finding max score (from player object)
    def sendWinnerAndClose(self):
        pass

    # Send snapchats to users inviting them to play
    def sendInvitationSnap(self, users):
        # invitation snap = some stuff
        # self.sendsnap(invitation snap, users, 10)
        pass

    # Simultaneously creates judge and player prompts,
    # saves them to state vars.
    def createPrompt(self):
        # player image = some stuff
        # judge image = some stuff
        # self.prompt = {'player': playerimage,
        #                'judge' : judgeimage}
        pass


    # Returns file path to player or judge prompt, based on
    # parameter passed in
    def getPrompt(judge=False):
        if judge:
            return self.prompt['judge']
        else:
            return self.prompt['player']

    # Sends question prompts to all players as well as judge
    def sendPromptMessages(self):
        self.createPrompt()
        playerpath = self.getPrompt(False)
        judgepath = self.getPrompt(True)
        nonjudges = [x['username'] for x in self.players if not x == self.judge]
        self.sendSnap(playerpath, ','.join(nonjudges), 10)
        self.sendSnap(judgepath, self.judge['username'], 10)


    # Check to see if all unconfirmed players have accepted
    # Starts game if true
    def checkForAccepts(self):
        unconfirmedPlayers = [x for x in self.players
                if x['confirmed'] == False]
        if (len(unconfirmedPlayers) == 0):
            self.gameRound = 1
            self.players[0]['winner'] = None;
            self.players[0]['judged'] = true
            currentJudge = self.players[0]

    # Enters judging mode, sends all choices to judge
    def proceedToJudging(self):
        recipient = self.judge['username']
        for entry in self.entries:
            path = 'snaps/' + entry['id'] + '.jpg'
            time = entry['time']
            self.sendSnap(path, recipient, time)

    # Initializes the round
    def startRound(self):
        self.roundStage = RoundStage.Entries
        self.sendPromptMessages()
        self.roundStart = time.time()

    # gets all new snaps, and returns a list of them
    def pollAndFetchSnaps(self):
        playernames = [x['username'] for x in self.players]
        snaps = [x for x in s.get_snaps()
                if x['status'] == 1 # Unopened
                and playernames.index(x['sender']) != -1
                and x['media_type'] == 0  # Is a photo, not a video
                ]

        successfullyDownloaded = [];

        for snap in snaps:
            if self.fetchPhotoSnap(snap['id']):
                successfullyDownloaded.append(snap)

        return successfullyDownloaded

    # Sends friend requests and invitations to all players
    def friendPlayers(self):
        friendslist = [x['name'] for x in self.api.get_friends()]
        toadd = [x['username'] for x in players
                if not friendslist.index(x['username']) == -1]
        for user in toadd:
            self.api.add_friend(user)

        self.sendInvitationSnaps(','.join(toadd));

    # Prints a list of current players
    def printPlayers(self):
        for p in self.players:
            print p['username']

    # Prints a list of all snaps that are available to download
    def listSnaps(self):
        snaps = [x for x in s.get_snaps() if x['status'] == 1]
        pprint(snaps)

    # Downloads and saves the snap with id snapid
    def fetchPhotoSnap(self, snapid):
        name = "snaps/" + snapid + ".jpg"
        f = open(name, 'wb')
        blob = self.api.get_blob(snapid)
        if blob == None:
            f.close()
            return False
        else:
            f.write(blob)
        f.close()
        return True

    # Sends a snapchat stored at path to recipients
    # recipients should be comma separated (no space!) list of usernames
    def sendSnap(self, path, recipients, time=5):
        mediaid = self.api.upload(path)
        self.api.send(mediaid, recipients, time)
