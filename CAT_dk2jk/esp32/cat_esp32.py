''' CAT Modul für ESP32 '''

''' -----hier anpassen -----'''
baudrate      = 38400
''' ------------------------'''

from time    import sleep
from machine import UART,Pin

taste = Pin(21,Pin.IN,Pin.PULL_UP)
led   = Pin(20,Pin.OUT)
ser   = UART(1)
ser.init(baudrate=38400,tx=10,rx=9,timeout=100) # ms
   
def _read_all():
    sleep(.01)
    buffer =''
    n = ser.any()
    buffer= ser.read(n).decode()  
    return buffer

def write( cmd=';'):
    print(f'write: {cmd}')
    ser.write(cmd.encode()) # to ascii
    sleep(.2)    

def get(cmd='MD0;'):   
    write(cmd)
    s= _read_all()
    print(f'  get: {s}')
    return s
    
def close():
    pass
