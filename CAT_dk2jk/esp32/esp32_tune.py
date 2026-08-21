#!/usr/bin/env python3
''' YAESU FT-710
Ansteuerung eines externen
automatischen Tuners ( hier SG-230 )
dk2jk 30.03.2026 'Python 3.12.3'
'''
from time import sleep
from cat_esp32 import led,taste,get,write
tune_dauer = 2 # sekunden

def tune_function():
    meter = get('MS;')  # 'Meter'- Einstellung lesen
    mode  = get('MD0;') # 'Mode' lesen
    power = get('PC;')  # 'Power' lesen
    afgain= get('AG0;')  # 'AF GAIN' lesen
    beep = get('EX030101;') # 'beep' lesen
    write('EX030101050;')  # beep auf laut , falls aus
    write('AG0000;')    # lautstärke aus
    write('MS50;')      # 'Meter'- Einstellung auf 'SWR' stellen
    write('PC010;')     # 'Power' auf 10 Watt schalten
    write('MD06;')      # 'Mode' auf RTTY schalten
    write('MX1;')       # 'PTT' einschalten
    sleep(tune_dauer)   # x Sekunden lang Träger senden
    write('MX0;')       # 'PTT' ausschalten
    write( mode )       # die gelesenen Werte wieder herstellen
    write( power)
    write( meter )
    write( afgain )
    write ( beep )
    close()             # Schnittstelle schliessen
    return

while True:   
    x= taste()  # taste lesen , low aktiv 
    led(x)      # led an solange taste gedrueckt ist
    if x ==0:   # taste gedrueckt ?
        tune_function()
        
    