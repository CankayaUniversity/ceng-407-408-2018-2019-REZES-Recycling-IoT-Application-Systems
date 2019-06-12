import sys, os
import signal
import datetime
import json
import firebase_admin
from firebase_admin import credentials, auth, db


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

#this is for terminating the program while clicking ctrl-c
signal.signal(signal.SIGINT, signal_handler)
cwd = os.getcwd()
parentcwd = os.path.dirname(cwd)
sys.path.append(cwd)
sys.path.append(parentcwd)
print(sys.path)
#credentials of Firebase. We have downloaded a json file from firebase where our secret keys of connection exists.

#temporary variables until the code is complete
metal = 2
plastic = 7
glass = 3
unidentified = 2
machineName = "makina01"
userName = "rahan86"
currentUserPoints = db.reference("users1").child("rahan86").child("totalPoints").get()
#This is where we calculate the total point of a transaction.
def calculatePoints(metal, plastic, glass):

    earnedPoint = (metal * 2.5) + (plastic * 2) + (glass * 1.5)

    return earnedPoint

#This is where we create transactions and push them into firebase
def createTransaction():
    date = datetime.datetime.now()
    # json.dumps(date)
    #We create a Json Object so that we can push the required data into Firebase
    t1 = {
        "metal": metal,
        "plastic": plastic,
        "glass": glass,
        "userName": userName,
        "unidentified": unidentified,
        # "date": date,
        "machineName": machineName,
        "pointEarned": calculatedPoints

    }
    deneme1 = db.reference("transactions").push(t1)
    print(deneme1)


calculatedPoints = calculatePoints(metal, plastic, glass)
createTransaction()
#we update the current users total points in order to calculate the leaderboards in advance
deneme = db.reference("users1").child("rahan86").child("totalPoints").set(calculatedPoints + currentUserPoints)
print(deneme)
deneme2 = db.reference("users1").get()
for x in deneme2:
    if x == "rahan86":
        print ("succes")
    # print(x)
# while True:
#     try:
#
#
#     finally:
#         pass
