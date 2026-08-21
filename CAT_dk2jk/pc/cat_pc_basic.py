'''
CAT- Steuerung Basic.
Modul zur CAT- Steuerung des YAESU FT-710 über USB Schnittstelle.
Die Schnittstelle wird geöffnet beim Import des Moduls.
Die einzige Funktion 'cat' schreibt ein Cat-Kommando und liest die
zugehörige Antwort. Kommandos sind ASCII-mit ';' am Ende,
siehe 'YAESU FT-710 CAT Operation Reference Manual'

dk2jk 5.2026
'''
import serial 
import time 

port = '/dev/ttyUSB1'          # hier anpassen
baud = 38400

my_ser = serial.Serial( port, baud )

def cat( cmd = 'fa;'):
    my_ser.write(cmd.encode())  # ascii in bytes umwandeln und senden
    time.sleep(0.2)             # etwas warten
    antwort = my_ser.read_all() # und antwort lesen
    return antwort.decode()     # bytes in ascii umwandeln
