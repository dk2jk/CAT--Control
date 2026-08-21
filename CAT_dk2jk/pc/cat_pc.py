''' YAESU FT-710 Ansteuerung eines externen
    automatischen Tuners ( hier SG-230 )
    dk2jk 30.03.2026 'Python 3.12.3'
'''
from   serial import Serial # erfordert installation von pyserial
import sys
from   time   import sleep
import get_serial_ports as ports # portnamem feststellen

''' ----- hier evtll.  anpassen -----'''
baudrate = 38400
cat      = None


''' schnittstelle oeffnen'''
def serial_open(port):
    global cat
    cat = Serial(port, baudrate, timeout = .1, write_timeout= .1)

''' schnittstelle schliessen'''
def close():
    cat.close()

''' cat rx buffer lesen und damit leeren'''
def read():
    return cat.read_all().decode()

''' absenden und antwort lesen'''
def get(kommando): 
    write(kommando)
    return read()

''' kommando schreiben und den rx-Daten etwas zeit geben'''
def write(kommando):
    y=cat.write(kommando.encode())
    sleep(.2)
    return y

''' testen, ob schnittstelle richtig antwortet'''
def check_ok():
    '''buffer leeren'''
    read() 
    write(';') 
    if read() == '?;' :
        ok=True
    else:
        ok= False
    return ok
    
def check_ports():
    print(f'    Script  = "{ sys.argv[0] }" *******')
    com_ports = ports.get_com_ports()
    if len(com_ports)==0:
        abbruch_durch_fehler(f'*** keine Serial-Ports gefunden ***')
    port= com_ports[0] # der erste passt wahrscheinlich
    print(f'Serial-Port = "{port}" ' )
    serial_open(port)
    if check_ok():
        y=True
    else:
        y=False
    return y

