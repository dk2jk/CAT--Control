# importe --------------------------------
import signal
import sys
from   time import sleep,strftime,gmtime
from   icom import Icom
from   kxpa import Kxpa

import mqtt
from   timer_raspi  import Timer
from   schalten     import schalte, digOut
import aus_4relais
del    aus_4relais

#serielle schnittstellen
#icom= Icom( port='/dev/ttyUSB0', adr= 0xa4)
icom= Icom( port='/dev/ttyACM0', adr= 0xa4 , debug=False)
kxpa= Kxpa( port='/dev/ttyUSB0' )

sekunden_takt = Timer(sec=1.0)

def get_forward_power():
    '''RESPONSE format: ^PFnnnn; where nnnn is the
    forward power output of the amplifier, in tenths of
    watts. For example, ^PF1234; is 123.4 watts.'''
    
    x=kxpa.get_cmd('^PF;')
    #print(f'forward   power {x}')
    s= x.decode()
    try:
        y = int(s[3:7],10)/10
    except:
        y=0
    return y
    
def get_kxpa_swr():
    x=kxpa.get_cmd("^SW;")  #b'^SW010;'
    x= x.decode()   # '^SW010;'
    s= x[3:6]
    try:
        swr= int(s)/10
    except:
        swr= 1.99
    p= get_forward_power()
    if p >10:
        y=f'KXPA: SWR={swr}'
    else:
        y=f'KXPA: SWR  ---'
    return y


''' antennen name in abhängigkeit von antennen nr '''
# im blockschaltbild von rechts nach links
# { antennennr : antennenname }
ant_name= { 0:'unbekannt',
         1:'KW: G5RV/MV6',
         2:'2m horizontal',
         3:'2m vertical',
         4:'70cm vertikal',
         5:'70cm_horizo.',
         }

''' pa_name  in abhaengigheit von ptt stellung '''
pa_name = { 'aus': 'keine',
            'kw' : 'Kw: KXPA-100',
            'uhf': '70cm: TLA-435',
            'vhf': '2m: HLV-400'}

''' liefert zeit im format "05.Jun.2025 16:24:04 UTC" '''
def get_utc():
    return strftime("%d.%b.%Y %H:%M:%S UTC", gmtime())

print(get_utc())

''' Handler-Methode: Signal für KeyboardInterrupt oder Process kill abfangen '''
''' damit bei abbruch ein definierter zustand herrscht ''' 
def sigint_handler(signal, frame):
    digOut.clear() # relais , ptt, k4
    mqtt.client.publish('frequenz'  ,'frequenz?')
    mqtt.client.publish('antennen-name'    ,'antennen-name?')
    mqtt.client.publish('pa-name','pa-name')
    if signal ==32:
        s=f'Control C'
    elif signal==15:
        s=f'pkill python3'
    elif signal==9:
        s=f'bash stop from node red'
    else:
        s=f'exit nr:{signal}\n{frame}'      
    RED='\033[31m'
    NC='\033[0m'
    print(f'{RED} Process finished with {s} {NC} ')
    sys.exit(0) # endgültiger abbruch des programms
    
def interrupts_registieren():
    # SignalHandler registrieren:
    # bei thonny NIEMALS stop verwenden sondern Control C
    signal.signal(signal.SIGINT , sigint_handler)   # Control C
    signal.signal(signal.SIGTERM , sigint_handler)
    #signal.signal( signal.SIGKILL, sigint_handler) # geht nicht

                  
def kxpa_frequenz_schreiben(f):
    ''' wenn Frequenz geändert wurde '''
    '''    und im Kurzwellenband liegt '''
    '''    Frequenz an KXPA senden '''
    if ( f  >1_000 and f  < 52_000 ):
        kxpa.set_frequenz(f)
        
''' voreinstellung der angewählten Buttons '''               
def set_default_buttons():
    mqtt.client.publish('polarisation-bei-start','v')
    mqtt.client.publish('pa-freigabe-bei-start' ,'n')
    mqtt.client.publish('info' ,'gestartet...')
    # @@ info 19.aug.25 startet mit "PA Aus"
    
def startup():
    interrupts_registieren()
    ''' subscribed topics ( dass will ich mitbekommen ) '''
    mqtt.topic = {'pa-freigabe' :'n', 'polarisation': 'v' }
    mqtt.start_client()
    sleep(1)
    set_default_buttons()
    
def loop():       
    ''' checks for new messages von mqtt / node red'''
    mqtt.client.loop(timeout=1)
    ''' die 2 daten von den buttons holen        ''' 
    pa_freigabe     =  mqtt.topic['pa-freigabe']
    ant_polarisation = mqtt.topic['polarisation']
    ''' einmal in der sekunde '''
    if sekunden_takt():
        ''' frequenz via cat lesen - hier in khz '''
        ''' bei fehler ficom = 9x                '''
        ficom = icom.frequenz()
        #print('f_von_ICOM -->',ficom)
        ''' frequenz an kxpa senden '''      
        y=kxpa.set_frequenz(ficom)
        #print('f_an_kxpa -->',y)
        ''' weiter arbeiten mit frequenz in Mhz ( Float ) '''
        fmhz=ficom/1000.
        ''' hier action ! schalte relais fuer ptt und antennen '''
        bereich, afu_band_nr,ant_nr = schalte(fmhz,ant_polarisation,pa_freigabe=='j')
        
        ''' anzeigewerte an das Dashboard senden '''
        if fmhz <0.1:   # 9x
            fdisplay='-----'
            #mqtt.client.publish('info' ,icom.info)
            info1= f'ICOM: {icom.info}'
            
        else:
            fdisplay=format (fmhz,'.3f') # 3 stellen hinterm komma - evtll auch nullen
            #mqtt.client.publish('info' ,'Kommunikation OK')
            info1='ICOM: Kommunikation OK'

        info2= get_kxpa_swr()
        info= f'{info2}\n{info1}'

        mqtt.client.publish('info' ,info)
        mqtt.client.publish('frequ'  ,fdisplay)
        if afu_band_nr>=0 and pa_freigabe =='j':
            paName= pa_name[bereich]
        else:
            paName= pa_name['aus']
        mqtt.client.publish('pa-name', paName)
        mqtt.client.publish('ant', ant_name[ant_nr ]  )
        mqtt.client.publish('utc', get_utc() )
        
        
# hier gehts los...         
startup()
while True:
    loop()
