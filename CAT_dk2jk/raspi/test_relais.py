''' test der relais am i2c- port expander '''
''' und er zusatzrelais am raspi pin [5,6,13,19] '''
from time import sleep
from pcf8574 import  PCF8574
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
rel= [5,6,13,19]       # raspi port nummern der zusatzrelais


xout=PCF8574(adr=0x38) # relais am port expander
xout.write(255)        # alle aus   high = aus
for i in [0,1,2,3,4,5,6,7]:
    sleep(.1)
    xout.pin(i,0)      # der reihe nach einschalten
for i in [0,1,2,3,4,5,6,7]:
    sleep(.1)
    xout.pin(i,1)     # der reihe nach ausschalten

for i in rel:         # raspi port fuer zusatzrelais auf ausgang
    GPIO.setup(i,GPIO.OUT)
    
for i in rel:
    GPIO.output(i,0)  # der reihe nach einschalten
    sleep(.5)
for i in rel:
    GPIO.output(i,1)  # der reihe nach ausschalten
    sleep(.5)