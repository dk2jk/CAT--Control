from serial import Serial
from time   import sleep

def to_hex(l):
    l= list(l)
    yh=''
    for i in l: # zum drucken
        s= f'{i:02x} '.upper()
        yh=yh+s
    return yh

baudrate = 9600
# ICOM protokoll für Frequenz lesen:
cat_adr          = 0xa4  # ic-705
#kopf             = [0xFE, 0xFE, adr , 0xE0]
#cmd_frequenz     = [0x03]
abschluss        = [0xFD]
#frequenz_kommando = [0xFE, 0xFE, cat_adr, 0xE0] + [0x03] + [0xFD]
                    # kopf                       + f?     + abschluss




def read_frequenz_IC_705():
    kommando = [0xFE, 0xFE, 0xa4, 0xE0] + [0x03] + [0xFD]
    print( f'CAT-Kommando = {to_hex(kommando)}')
    my_ser   = Serial('/dev/ttyACM0', baudrate)
    my_ser.write( bytes(kommando) )
    
    antwort  = my_ser.read_until(bytes(abschluss))   
    print( f'Antwort      = {to_hex(antwort)}')
    
    nutzdaten= antwort[5:-1]
    print( f'Nutzdaten    = {to_hex(nutzdaten)}')
    
    nutzdaten_rueckwaerts =nutzdaten[::-1]
    print( f'Nutzdaten    = {to_hex(nutzdaten_rueckwaerts)}(gedreht)')
    
    text = bytes.hex(nutzdaten_rueckwaerts).upper()
    print(f'Roh-Ergebnis = "{text}" (als String)')
    mhz = float(text)/1e6
    print(f'Frequenz     = {mhz} MHz')
    my_ser.close()
    return mhz


if __name__ == '__main__':
    read_frequenz_IC_705()  

