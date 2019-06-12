import Tkinter as tk
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import sys
import sys, os
import signal
import datetime
import json
import firebase_admin
from firebase_admin import credentials, auth, db

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def calculatePoints(metal, plastic, glass):

    earnedPoint = (metal * 2.5) + (plastic * 2) + (glass * 1.5)

    return earnedPoint

#This is where we create transactions and push them into firebase
def createTransaction():
    now = time.strftime("%c")
    # json.dumps(date)
    #We create a Json Object so that we can push the required data into Firebase
    t1 = {
        "metal": matCounter.metal,
        "plastic": matCounter.plastic,
        "glass": matCounter.glass,
        "userName": matCounter.userName,
        "unidentified": matCounter.unidentified,
        "date": now,
        "machineName": "Makine1",
        "pointEarned": matCounter.calculatedPoints

    }
    deneme1 = db.reference("transactions").push(t1)
    print(deneme1)



#this is for terminating the program while clicking ctrl-c
signal.signal(signal.SIGINT, signal_handler)
cwd = os.getcwd()
parentcwd = os.path.dirname(cwd)
sys.path.append(cwd)
sys.path.append(parentcwd)
print(sys.path)
#window.maxsize(550,400)
#window.state("zoomed") # fullscreen yapar

    
class matCounter:
    plastic = 0
    metal = 0
    glass = 0
    unidentified = 0
    userName = " "
    calculatedPoints = 0

def qrWin():
    try:
       
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)  # servo motor pini
        GPIO.setup(11, GPIO.OUT)  # dc motor pini
        d = GPIO.PWM(11, 40)
        p = GPIO.PWM(7, 60)
        d.start(7.5)
        p.start(7.5)
        
        def firebaseSend():
            #cred = credentials.Certificate("/home/pi/Downloads/rezes-d49cc-firebase-adminsdk-tmwrp-d4c177d45f.json")
            #app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://rezes-d49cc.firebaseio.com'})
            #credentials of Firebase. We have downloaded a json file from firebase where our secret keys of connection exists.

            #temporary variables until the code is complete
            machineName = "makina01"
            matCounter.userName = db.reference("temp").get()
            currentUserPoints = db.reference("users1").child(matCounter.userName).child("totalPoints").get()
            #This is where we calculate the total point of a transaction.



            matCounter.calculatedPoints = calculatePoints(matCounter.metal, matCounter.plastic, matCounter.glass)
            createTransaction()
            #we update the current users total points in order to calculate the leaderboards in advance
            deneme = db.reference("users1").child(matCounter.userName).child("totalPoints").set(matCounter.calculatedPoints + currentUserPoints)

            
        def ORB(input_image, stored_image):

            gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

            orb_detector = cv2.ORB(1600, 1.3)

            (keypoints_1, descriptor_1) = orb_detector.detectAndCompute(gray, None)

            (keypoints_2, descriptor_2) = orb_detector.detectAndCompute(stored_image, None)

            brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matches_found = brute_force.match(descriptor_1, descriptor_2)

            matches_found = sorted(matches_found, key=lambda val: val.distance)

            return len(matches_found)

        def detGlass():
            temp = 0
            capture = cv2.VideoCapture(1)

            stored_image = cv2.imread('cam.jpg', 0)

            glass_count = 0

            n = 0
            while n < 10:
                n += 1
                ret, capturing = capture.read()

                frame_height, frame_width = capturing.shape[:2]

                x1_top_left = frame_width / 3
                y1_top_left = (frame_height / 2) + (frame_height / 4)
                x2_bottom_right = (frame_width / 3) * 2
                y2_bottom_right = (frame_height / 2) - (frame_height / 4)

                ### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)

                cropped_box = capturing[y2_bottom_right:y1_top_left, x1_top_left:x2_bottom_right]
                capturing = cv2.flip(capturing, 1)
                matches_found = ORB(cropped_box, stored_image)
                string = "Matches Found = " + str(matches_found)

                cv2.putText(capturing, string, (150, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                set_threshold = 350
                if matches_found > set_threshold:
                    glass_count += 1
                # resized_frame = cv2.resize(capturing, (250, 250))
                # gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
                # path = './glass_count/' + str(glass_count) + '.jpg'
                # cv2.imwrite(path, gray)
                # cv2.putText(gray, str(glass_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                # cv2.imshow('Detection', gray)

                # cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

                # cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

            # cv2.imshow('Glass_Detection', capturing)

            # c = cv2.waitKey(1)

            capture.release()
            # cv2.destroyAllWindows()
            if glass_count > 3:
                temp = 1
            return temp

        def detMetal():
            temp = 0
            capture = cv2.VideoCapture(1)

            stored_image = cv2.imread('cocacola.jpg', 0)

            metal_count = 0

            n = 0
            while n < 10:
                n += 1
                ret, capturing = capture.read()

                frame_height, frame_width = capturing.shape[:2]

                x1_top_left = frame_width / 3
                y1_top_left = (frame_height / 2) + (frame_height / 4)
                x2_bottom_right = (frame_width / 3) * 2
                y2_bottom_right = (frame_height / 2) - (frame_height / 4)

                ### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)

                cropped_box = capturing[y2_bottom_right:y1_top_left, x1_top_left:x2_bottom_right]
                capturing = cv2.flip(capturing, 1)
                matches_found = ORB(cropped_box, stored_image)
                string = "Matches Found = " + str(matches_found)

                cv2.putText(capturing, string, (150, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                set_threshold = 350
                if matches_found > set_threshold:
                    metal_count += 1
                # resized_frame = cv2.resize(capturing, (250, 250))
                # gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
                # path = './metal_count/' + str(metal_count) + '.jpg'
                # cv2.imwrite(path, gray)
                # cv2.putText(gray, str(metal_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                # cv2.imshow('Detection', gray)

                # cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

                # cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

            # cv2.imshow('Metal_Detection', capturing)

            # c = cv2.waitKey(1)

            capture.release()
            # cv2.destroyAllWindows()
            if metal_count > 3:
                temp = 2
            return temp

        def detPet():
            temp = 0
            capture = cv2.VideoCapture(1)

            stored_image = cv2.imread('Pet.jpg', 0)

            pet_count = 0

            n = 0
            while n < 10:
                n += 1
                ret, capturing = capture.read()

                frame_height, frame_width = capturing.shape[:2]

                x1_top_left = frame_width / 3
                y1_top_left = (frame_height / 2) + (frame_height / 4)
                x2_bottom_right = (frame_width / 3) * 2
                y2_bottom_right = (frame_height / 2) - (frame_height / 4)

                ### cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,0,255), 4)

                cropped_box = capturing[y2_bottom_right:y1_top_left, x1_top_left:x2_bottom_right]
                capturing = cv2.flip(capturing, 1)
                matches_found = ORB(cropped_box, stored_image)
                string = "Matches Found = " + str(matches_found)

                cv2.putText(capturing, string, (150, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                set_threshold = 1
                if matches_found > set_threshold:
                    pet_count += 1
            #	resized_frame = cv2.resize(capturing, (250, 250))
            #	gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            #	path = './pet_count/' + str(pet_count) + '.jpg'
            #	cv2.imwrite(path, gray)
            #	cv2.putText(gray, str(pet_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            #	cv2.imshow('Detection', gray)

            #	cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)

            #	cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)

            #	cv2.imshow('Pet_Detection', capturing)

            #	c = cv2.waitKey(1)

            capture.release()
            # cv2.destroyAllWindows()
            if pet_count > 5:
                temp = 3
            return temp

        def dropMaterial():

            d.ChangeDutyCycle(2.5)
            time.sleep(2)
            d.ChangeDutyCycle(7.5)
            time.sleep(1)
            p.ChangeDutyCycle(7.5)
            return True

        # servo motoru harekete gecer. materialID degiskeni gelen material tipini belirler.
        # | materialID = 0 (metal)    |
        # | materialID = 1 (plastic)  |
        # | materialID = 2 (glass)    |
        # | materialID = 3 (undefined)|
        def runServo(materialID):

            # material id burada tanimlanacak.
            # p.ChangeDutyCycle(7.5)
            try:
                if (materialID == 0):
                    p.ChangeDutyCycle(7.5)  # start
                elif (materialID == 1):
                    p.ChangeDutyCycle(12.5)  # 180 derece
                elif (materialID == 2):
                    p.ChangeDutyCycle(2.5)  # 0 derece
                elif (materialID == 3):
                    p.ChangeDutyCycle(5.5)  # Undefined malzemeler icin
                time.sleep(1)
                dropMaterial()

                return True
            except KeyboardInterrupt:
                p.stop()
                GPIO.cleanup()
                print("Servo motor error")
                return False

        window = tk.Tk()
        window.title("RESEZ")

        window.geometry("1024x600")
        # window.resizable(FALSE,FALSE)
        # window.maxsize(550,400)
        # window.state("zoomed") # fullscreen yapar

        title = tk.Label(text="Welcome " + db.reference("users1").child(db.reference("temp").get()).child("name").get() +" " + db.reference("users1").child(db.reference("temp").get()).child("surname").get() , fg="red")
        title.pack()
        photo = tk.PhotoImage(file="REZESLogo1.png")
        label = tk.Label(window, image = photo)
        label.pack()
        def exit_btn():
            firebaseSend()
            window.destroy()
            
            


        butonex = tk.Button(window,text="EXIT", bg = "green" , bd=1, relief="solid", anchor = tk.CENTER , font = "Times 38", width=12,height=3, fg = "white", command= exit_btn)
        butonex.place(x = 576, y = 350)
        def caglarMethodisHere():
            if detGlass() == 1:
                matID = 1
                matCounter.glass += 1
                print("Glass")
            elif detMetal() == 2:
                matID = 2
                matCounter.metal += 1
                print("Metal")
            elif detPet() == 3:
                matID = 3
                matCounter.plastic += 1
                print("Pet")
            else:
                matID = 0
                matCounter.unidentified += 1
                print("Undif")
            runServo(matID)

        buton = tk.Button(window, text="CONFIRM",bd=1 , bg = "green", relief="solid", anchor = tk.CENTER , font = "Times 38", width=12,height=3, fg = "white",
                          command=caglarMethodisHere)
        buton.place(x = 100, y = 350)
        
        window.mainloop()
    except: 
        print("Exception occured!!")
        #logger.error(str(e))
        
    finally :
        GPIO.cleanup()
        

#mainScreen()
qrWin()
