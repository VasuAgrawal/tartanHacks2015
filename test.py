from pprint import pprint
from pysnap import Snapchat

s = Snapchat()
s.login('snapsvshumanity', 'ilovetosnap69')
snaps = [x for x in s.get_snaps() if x['status'] == 1]

pprint(snaps)

for currentSnap in snaps:
    snapid = currentSnap['id']
    f = open('snaps/' + snapid + '.jpg', 'wb')
    blob = s.get_blob(snapid)
    if blob != None: f.write(blob)
    f.close()

# mediaid = s.upload('snaps/' + snaps[0]['id'] + '.jpg')

#mediaid = s.upload('hax.jpg')

#print mediaid
#s.send(mediaid, 'snapsvshumanity')
