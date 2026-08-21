# zusatz relais
from time import sleep

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

rel= [5,6,13,19]
for i in rel:
    GPIO.setup(i,GPIO.OUT)

print ( '4 relais in ruhezustand gesetzt , Ausgänge =HIGH')
for i in rel:
    GPIO.output(i,1)
    sleep(.5)

