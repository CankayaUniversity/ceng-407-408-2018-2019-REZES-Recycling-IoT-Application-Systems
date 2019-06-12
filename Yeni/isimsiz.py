import RPi.GPIO as GPIO
import Tkinter as tk
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)




def runServo():
	GPIO.output(11,GPIO.HIGH)
	time.sleep(4)


window = tk.Tk()
window.title("RESEZ")

window.geometry("550x400+250+100")

title = tk.Label(text = "Hos Geldiniz.", fg = "red")
title.pack()

myID = 1

buton = tk.Button( text = "Onayla",
                command = runServo)
buton.pack()

window.mainloop()
