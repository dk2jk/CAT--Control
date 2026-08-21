''' Schnittstelle fuer KXPA100 '''
from serial import Serial

def erzeuge_frequenz_kommando(frequenz=3587):
    '''erzeuge_frequenz_kommando(frequenz)
    input: frequenz [khz]
    output: Command string für kxpa z.b.: b'^MT03587;' '''
    # grobe begrenzung auf kurzwelle...
    frequenz= int(frequenz) # falls eingabe in float
    if frequenz < 1000 or frequenz > 60000 : 
        cmd_frequenz =b';'   # null Kommando
    else:
        frequenz_string = str(frequenz).zfill(5)        # 03587  ... 5 stellen mit führende nullen     
        frequenz_bytes  = frequenz_string.encode()      # b'03587'
        cmd_frequenz    = b'^MT' + frequenz_bytes + b';'  # b'^MT03587;'
    return cmd_frequenz  

class Kxpa():
    def __init__( self,*, port):
        self.port=port
    
    def get_cmd(self,cmd_string):   # "^AEA;" mit semicolon
        try:
            serial= Serial(self.port,baudrate=38400,timeout=3)
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x[0:x.index(':')])
            return '*** fehler serial ***'
        cmd    = cmd_string.encode() 
        serial.write(cmd)
        response=serial.read_until(b';')
        serial.close()
        return response
    
    def set_cmd(self,cmd_string):   # "^AEA;" mit semicolon
        try:
            serial= Serial(self.port,baudrate=38400,timeout=3)
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x[0:x.index(':')])
            return '*** fehler serial ***'
        cmd    = cmd_string.encode() 
        serial.write(cmd)
        response=serial.read_until(b';')
        serial.close()
        return response
    
    def get_id(self):
        try:
            serial= Serial(self.port,baudrate=38400,timeout=3)
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x[0:x.index(':')])
            return '*** fehler serial ***'
            
        cmd_id    = b'^I;' 
        serial.write(cmd_id)
        response=serial.read_until(b';')
        serial.close()
        return response
        
        
    def set_frequenz(self, khz ):   
        '''set_frequenz( port , khz ):
        port = 'dev/ttyxxx'
        khz         = Frequenz in kHz ( Integer)
        Kommando wird aufbereitet:
        ^MT (ATU Memory Recall Tune, SET only)
        to perform a memory recall tune on a frequency
        ^MTfffff; where fffff is a frequency, in kHz.
        '''
        try:
            serial= Serial(self.port,baudrate=38400,timeout=3)
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x[0:x.index(':')])
            return '*** fehler serial ***'
            
        kommando= erzeuge_frequenz_kommando(khz)
        serial.write(kommando)
        serial.close()
        return kommando
        
if __name__ == '__main__':
    kxpa= Kxpa( port='/dev/ttyUSB0')
    x=kxpa.get_cmd('^RV;')
    print(f'revision : {x}')        # b'^RV01.39;' 
    x=kxpa.get_cmd('^SN;')
    print(f'serialNr : {x}')        # b'^SN00195;'
    x=kxpa.get_id() # get identifier
    print(f'ident    : {x}')        # b'^IKXPA100;'
    x=kxpa.set_cmd('^OP;') 
    print(f'Status   : {x}')        #  b'^OP0;' = standby, b'^OP1;' =operate
    x=kxpa.get_cmd("^AEA;")
                    # antenna enable
    print(f'Ant enabled: {x}')        # b'^AEA33333333333;' ant1 und 2  freigegeben
    x=kxpa.get_cmd("^SB;")
    print(f'bypass    SWR {x}')        # b'^SB010;' atu bypass swr
    '''^SB is the SWR of the antenna, as measured at the KXPA100 coupler, when the KXAT100 Antenna Tuner
    was last in bypass (which occurs in each full search tune).
    '''
    x=kxpa.get_cmd("^SW;")
    print(f'aktuelles SWR {x}')        # b'^SW010;' atu swr
    x=kxpa.get_cmd('^PF;')
    print(f'forward   power {x}')        # b'^PF0000;' power forward
    x=kxpa.get_cmd('^PV;')
    print(f'reflected power power {x}')
    ''' RESPONSE format: ^PVnnnn; where nnnn is the reflected power from the antenna connector, in tenths
    of watts. For example, ^PV0034; indicates a reflected power of 3.4 watts.
    '''
    x=kxpa.get_cmd('^PD;')
    print(x)        # b'^PD0000;' power dissipation
    x=kxpa.get_cmd('^PC;')
    print(x)        # b'^PC0000;' current *10
    x=kxpa.get_cmd('^MD;') 
    print(x)        # b'^MDA;' atu mode auto
    x=kxpa.get_cmd('^AT;') # atenunnuator settings
    print(x)        # b'^AT2;'    back panel switch
    
    x=kxpa.get_cmd('^LR;') # get inductors L
    print(x)
    x=kxpa.get_cmd('^CR;') # get capacitors C
    print(x)
    x=kxpa.get_cmd('^FL;') # get fault
    print(x)        # b'^FLN00001;'  N = None
    x=kxpa.get_cmd('^F;') # get last transmission frequency
    print(x)        # b'^F00000;'
    
   # x=kxpa.set_cmd('^MDA;') # set bybass atu (B)ypass /(M)anual / (A)utomatik
   # x=kxpa.set_cmd('^BYN;')  # set bybass atu  No / Bypass
   # x=kxpa.set_cmd('^OP1;') # ^OP  PA bypass  Operate  0=bypass 1= not bypassed
   
   # 20 jan 2026:
   # x= kxpa.get_cmd('^AEA33313333333;')  # auf 40m ( band 4 von 0...11) ANT1 waehlen ! 
    
 