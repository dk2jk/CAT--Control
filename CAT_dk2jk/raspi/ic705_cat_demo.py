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

#ICOM Kommando zum Frequenz lesen:
# FE FE A4 E0 03 FD
# FE FE             <- kopf
# ..... A4          <- IC-705 CAT Adresse
# ........ E0       <- default ??
# ........... 03    <- Kommando Frequenz lesen
# .............. FD <- Ende Zeichen


            






def read_frequenz_IC_705():
    kommando = [0xFE, 0xFE, 0xa4, 0xE0] + [0x03] + [0xFD]
    print( f'CAT-Kommando = {to_hex(kommando)} <= Frequenz lesen')
    my_ser   = Serial('/dev/ttyACM0', baudrate)
    my_ser.write( bytes(kommando) )
    
    antwort  = my_ser.read_until(bytes(abschluss))   
    print( f'Antwort      = {to_hex(antwort)}')
    
    nutzdaten= antwort[5:-1]
    print( f'Nutzdaten                   = {to_hex(nutzdaten)}')
    
    nutzdaten_rueckwaerts =nutzdaten[::-1]
    print( f'Nutzdaten                   = {to_hex(nutzdaten_rueckwaerts)}(gedreht)')
    
    text = bytes.hex(nutzdaten_rueckwaerts).upper()
    print(f'Roh-Ergebnis                ="{text}" = text')
    mhz = float(text)/1000_000
    print(f'Frequenz                    = {mhz} MHz = float(text)/1e6')
    my_ser.close()
    return mhz


if __name__ == '__main__':
    read_frequenz_IC_705()  

