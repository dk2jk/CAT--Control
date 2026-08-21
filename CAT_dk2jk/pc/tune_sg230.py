''' YAESU FT-710 Ansteuerung eines externen
    automatischen Tuners ( hier SG-230 )
    dk2jk 30.03.2026 'Python 3.12.3'
'''
import sys
from   time   import sleep
from cat_pc   import get,write,check_ports,close

tune_dauer = 2 # sekunden

''' Die Tune- Funktion '''
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

# ''' Die Tune- Funktion komprimiert '''
# def tune_function():
#     backup = get('MS;MD0;PC;AG0;EX030101;')  # Einstellung lesen
#     write('AG0000;MS50;PC010;MD06;MX1;')    # kommandos
#     sleep(tune_dauer)   # x Sekunden lang Träger senden
#     write('MX0;')       # 'PTT' ausschalten
#     write( backup )     # backup wieder herstellen
#     #close()             # Schnittstelle schliessen
#     return

''' Start '''
if __name__ == '__main__':
    check_ok = check_ports()
    if check_ok:
        tune_function()     # Tunen, wenn das Script gestartet wird (Icon)
        print ('ok')
        sleep(1)
        sys.exit()
    else:
        print(f'*** Serial-Port antwortet nicht ***')
        sleep(3)
        sys.exit(error)

