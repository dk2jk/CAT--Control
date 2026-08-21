import berechnungen as berechne
from pcf8574_v2 import PCF8574
digOut = PCF8574(adr=0x38)
from time import sleep
from icom import Icom
icom= Icom( port='/dev/ttyACM0', adr= 0xa4 )

startup_flag = True

class port:
    status = 0b_1111_1111

def schalte_ptt_aus():
    digOut.pin( 0, 1 )
    digOut.pin( 3, 1 )
    digOut.pin( 2, 1 )
    digOut.pin( 1, 1 )
    
def schalte_relais(rel):
    digOut.pin( 6, rel[0] )
    digOut.pin( 5, rel[1] )
    digOut.pin( 4, rel[2] )
    
def schalte_ptt(ptt):
    digOut.pin( 0, ptt[0] )
    digOut.pin( 3, ptt[1] )
    digOut.pin( 2, ptt[2] )
    digOut.pin( 1, ptt[3] )
   
def update_power(afu_band_nr,pa_enable, pol='h'):
    if pa_enable:
        if pol=='v' and (afu_band_nr == 11): #2m
             proz=50
        else:
            proz=100        
    else:
        proz=100
    icom.maxpower(proz)
    return proz   

def schalte(f,pol,pa_enable):
    global startup_flag
    ''' randbedingungen berechnen '''
    bereich     = berechne.bereich(f)
    afu_band_nr = berechne.afu_band_nr(f)
    ant_nr      = berechne.ant_nr(bereich,pol)

    ''' voreinstellung der ausgaenge berechnen '''
    rel  = berechne.relais_bits(ant_nr)
    ptt  = berechne.ptt_bits(afu_band_nr,pa_enable)
    #print(ptt)
    #print(rel)
    preset = berechne.preset(ptt,rel)
    #print (bin(preset)[2:].rjust(8,'0'))

    '''haben sich die Voreinstellungen geaendert ? '''
    if startup_flag:  # @@ info 19.aug.25 startet immer mit neueinstellung
        neu= True
        startup_flag=False
    else:
        neu = ( preset != port.status)

    if neu:
        #jetzt umschalten
        # 1. ptt aus
        sleep(.1)
        schalte_ptt_aus()
        x=update_power(afu_band_nr,pa_enable)
        print(f'power= {x} %')
        print (bin(digOut.read())[2:].rjust(8,'0'))
        sleep(.1)
        schalte_relais(rel)
        print (bin(digOut.read())[2:].rjust(8,'0'))
        sleep(.1)
        schalte_ptt(ptt)
        print (bin(digOut.read())[2:].rjust(8,'0'))
        
        ''' ausgefuehrt !'''
        port.status = preset
    return  bereich, afu_band_nr,ant_nr 
# ende def berechne    

if __name__ =='__xmain__':
    digOut.clear()
    f=3.6
    pol='h'
    pa_enable=True
    schalte(f,pol,pa_enable)
    

    
    