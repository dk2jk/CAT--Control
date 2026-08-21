
from serial import Serial    # modul serial laden

                                            # Kommentar mit Beispieldaten...
def read_frequenz_IC_705():	                # Frequenz lesen ...
    kommando = [0xFE, 0xFE, 0xa4, 0xE0]+  [0x03] + [0xFD]
                                            # FE FE A4 E0 03 FD  
    com   = Serial('/dev/ttyACM0', 9600)    # schnittstelle öffnen
    com.write( bytes(kommando) )            # kommando schreiben   
    antwort = com.read_until(bytes([0xFD])) # FE FE E0 A4 03 00 50 12 07 00 FD
    nutzdaten = antwort[5:9]                #                00 50 12 07 00
    nutzdaten_rueckwaerts =nutzdaten[::-1]  # (gedreht)      00 07 12 50 00 
    text = nutzdaten_rueckwaerts.hex()      # text =         "0007125000" 
    mhz = float(text)/1000_000              # mhz = float("0007125000")/1e6 
    com.close()                             # schnittstelle schliessen
    return mhz                              # ergebnis = 7.125

if __name__ == '__main__':
    frequenz = read_frequenz_IC_705()       # frequenz lesen
    print ( f' f={frequenz} MHz')           # und anzeigen:  f=7.125 MHz

