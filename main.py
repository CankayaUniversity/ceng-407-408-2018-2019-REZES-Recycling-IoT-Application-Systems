from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import sys, os
import signal
import datetime
import json
import firebase_admin
from firebase_admin import credentials, auth, db
# get the webcam:  
barCode = ""
cap = cv2.VideoCapture(0)
cred = credentials.Certificate("/home/pi/Downloads/rezes-d49cc-firebase-adminsdk-tmwrp-d4c177d45f.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://rezes-d49cc.firebaseio.com'})

print("afterExit")
cap.set(3,1024)
cap.set(4,600)
#160.0 x 120.0#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results-
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)
	
        print('Type : ', decodedObject.type)

        print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
       
        #print(barCode)
        #cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('REZESbYrhN',frame)
    
    cv2.waitKey(1)
    #key = cv2.waitKey(1)
    if (barCode != "") :
        
        deneme2 = db.reference("users1").get()
        #time.sleep(10)
        db.reference("temp").set(barCode)
        print(deneme2)
        for x in deneme2:
            print(x)
            #y = "b'" + x + "'"
            #print(y)
            if (x == barCode):
                #print(x)
                print ("succes")
                cap.release()
                cv2.destroyAllWindows()
                exec(open("firsttry.py").read())
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
