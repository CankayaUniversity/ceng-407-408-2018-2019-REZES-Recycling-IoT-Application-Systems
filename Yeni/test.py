import Tkinter as tk
import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)
GPIO.setup(7,GPIO.OUT) 
GPIO.setup(11,GPIO.OUT) 

p = GPIO.PWM(7,50)
p.start(7.5)

def dropMaterial():
    GPIO.output(11,GPIO.HIGH)
    time.sleep(4) 
    GPIO.output(11,GPIO.LOW)
    return  True

def runServo(materialID):
    p.ChangeDutyCycle(7.5)
    try:
        if(materialID == 0):
          p.ChangeDutyCycle(7.5) 
          time.sleep(5)
        elif(materialID == 1):
          p.ChangeDutyCycle(12.5)  
          time.sleep(5)
        elif(materialID == 2):
            p.ChangeDutyCycle(2.5)  
            time.sleep(5)
        elif(materialID == 3):
            p.ChangeDutyCycle(5.5) 
            time.sleep(5)
        dropMaterial()
        return True
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
        print("Servo")
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
    matID = 0
    print("k")
    checked = runServo(matID)
    if(checked):
        dropMaterial()
    else:
        print("islem failed")
myID = 1

buton = tk.Button( text = "Onayla",
                command = runServo(myID))
buton.pack()

tk.mainloop()
