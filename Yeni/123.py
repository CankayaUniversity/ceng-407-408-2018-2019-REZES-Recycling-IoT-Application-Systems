import Tkinter as tk
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

GPIO.setmode (GPIO.BOARD)
GPIO.setup(7,GPIO.OUT) #servo motor pini
GPIO.setup(11,GPIO.OUT) #dc motor pini
d = GPIO.PWM(11,50)
d.start(7.5)
p = GPIO.PWM(7,50)
p.start(7.5)

def dropMaterial():

    d.ChangeDutyCycle(2.5)
    time.sleep(2)
    d.ChangeDutyCycle(7.5)
    time.sleep(1)
    p.ChangeDutyCycle(7.5)
    return  True
#servo motoru harekete gecer. materialID degiskeni gelen material tipini belirler.
#| materialID = 0 (metal)    |
#| materialID = 1 (plastic)  |
#| materialID = 2 (glass)    |
#| materialID = 3 (undefined)|
def runServo(materialID):
    
	#material id burada tanimlanacak. 
    #p.ChangeDutyCycle(7.5)
    try:
        if(materialID == 0):
          p.ChangeDutyCycle(7.5) #start 
        elif(materialID == 1):
          p.ChangeDutyCycle(12.5)  # 180 derece
        elif(materialID == 2):
            p.ChangeDutyCycle(2.5)  # 0 derece
        elif(materialID == 3):
            p.ChangeDutyCycle(5.5) #  Undefined malzemeler icin
        dropMaterial()
        
        return True
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
        print("Servo motor error")
        return False



window = tk.Tk()
window.title("RESEZ")

window.geometry("550x400+250+100")
#window.resizable(FALSE,FALSE)
#window.maxsize(550,400)
#window.state("zoomed") # fullscreen yapar

title = tk.Label(text = "Hos Geldiniz.", fg = "red")
title.pack()

def caglarMethodisHere():
	matID = 1
	runServo(matID)
	dropMaterial()
	



buton = tk.Button( text = "Onayla",
                command = caglarMethodisHere)
buton.pack()
def ORB(input_image, stored_image):

	    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)


	    orb_detector = cv2.ORB(1600, 1.3)


	    (keypoints_1, descriptor_1) = orb_detector.detectAndCompute(gray, None)

	    (keypoints_2, descriptor_2) = orb_detector.detectAndCompute(stored_image, None)

	    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	    matches_found =  brute_force.match(descriptor_1,descriptor_2)


	    matches_found = sorted(matches_found, key=lambda val: val.distance)

	    return len(matches_found)

window.mainloop()
