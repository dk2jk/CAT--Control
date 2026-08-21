from serial import Serial

class power:
    watt =[0.5 ,1.0 ,2.5 ,5.0 ,10.0]
    code =[0x00,0x01,0x02,0x03,0x04]
    proz =[5   ,10  ,25  ,50  ,100 ]
    
class Icom(power):
    def __init__( self,*, port, adr , debug = False):
        self.adr=adr
        self.port=port
        self.debug=debug
        self.info = 'no info'
    
    def get_info(self):
        return self.info

    def frequenz(self):
        #response = b''
        ''' kommando zusammenstellen'''
        request = bytes ( [0xFE, 0xFE, self.adr , 0xE0, 0x03, 0xFD] )
        if self.debug:
            hex_bytes=bytes.hex(request).upper()
            print( f'gesendet: {hex_bytes} (Frequenzabfrage ic-705)' )
        try:
            serial= Serial( self.port, \
                    baudrate=9600, timeout=10, writeTimeout=10)
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x)   # [0:x.index(':')])
            self.info = x
            return 99  # fehlercodierung , kommt real nicht vor
        
        '''senden '''
        try:
            serial.write(request)
        except Exception as e:
            print(e)
            self.info = e
            return 98 # fehlercodierung , kommt real nicht vor
        
        try:
            if self.adr != 0xa4:
                response=serial.read_until(bytes([0xfd]))  #echo
                print(f'*** Test mit Icom 706, adr = {hex(self.adr)} ***')
            else:
                response=serial.read_until(bytes([0xfd]))
        except Exception as e:
            print(e)
            self.info = e
            return 99 # fehlercodierung , kommt real nicht vor
                
        serial.close()
        ng_message = b'\xfe\xfe\xe0\xa4\xfa\xfd'
        if response==b'': # nix da
            e= " *** no data ***"
            print (e)
            self.info = e
            return(92)    # fehlercodierung , kommt real nicht vor
        else:
            if response == ng_message:
                hex_bytes=bytes.hex(ng_message).upper()
                print( f'empfangen: {hex_bytes} (Antwort vom ic-705) ')
                s=f'***ERROR*** frequenz abfragen : antwort "NotGood" vom ic705'
                print(s)
                self.info = 'Power Off via Remote'
                khz=93 # fehlercodierung , kommt real nicht vor
            else:
                
                ''' daten interpretieren'''
                hex_bytes=bytes.hex(response)
                if self.debug:
                    print(f'von ICOM: {hex_bytes.upper()}')
                s=''
                for i in range(18,9,-2):
                    s=s+hex_bytes[i:i+2]
                if self.debug:
                    print(f'   Daten: {s}')   # s= "0438875000"
                try:
                    khz= int(int(s)/1e3)
                    if self.debug:
                        print(f'   [kHz]: {khz}')
                except:
                    self.info = 'falsches Datenformat'
                    khz=94 # fehlercodierung , kommt real nicht vor
            return khz


    def read_maxpower(self) -> int :
        proz=0
        if self.adr != 0xa4:
            proz= -1 #'*** kein ic-705 ***'
        else:
            cmd = bytes ([0xFE, 0xFE, self.adr , 0xe0, 0x1a, 0x05,0x00, 0x37, 0xFD])
            serial= Serial( self.port, \
                    baudrate=9600, timeout=3, writeTimeout=3 )    
            '''senden '''
            if self.debug:
                hex_bytes=bytes.hex(cmd).upper()
                print( f'gesendet: {hex_bytes} (maxpower abfrage ic-705)' )
            serial.write(cmd)
            response=serial.read_until(bytes([0xfd]))
            hex_bytes=bytes.hex(response)
            print(f'von ICOM: {hex_bytes}')
            index= response[8]
            proz= power.proz[index]
        return proz
    
    def maxpower(self,proz):
        ''' leistungbegrenzung des ic-705 einstellem
            port : Ser.Schnittselle #'/dev/ttyUSB0'
            adr  : Icom CI-V  0xa4 für ic705
            Return: ok/ Fehler als text
        '''
        if self.adr != 0xa4:
            return '*** kein ic-705 ***'
        
        ''' parameter fuer leistungsbegrenzung '''
        pow_code=0x04
        if proz>=100:
            proz=100
            pow_code=0x04
        elif proz >= 50: 
            proz=50
            pow_code=0x03
        elif proz >= 25:
            proz=25
            pow_code=0x02
        elif proz >= 10:
            proz=10
            pow_code=0x01
        else :
            proz=5
            pow_code=0x00
        
        ''' kommandodaten zusammenstellen '''
        cmd = bytes ([0xFE, 0xFE, self.adr , 0xe0, 0x1a, 0x05,0x00, 0x37, pow_code, 0xFD])
        ''' ser. schnittstelle offnen '''
        try:
            serial= Serial( self.port, \
                    baudrate=9600, timeout=3, writeTimeout=3 ) 
        except Exception as e:
            ''' fehler ser. schnittstelle '''
            x= e.args[1]
            print(x[0:x.index(':')])
            self.info = e
            return '*** fehler serial ***'
    
        '''senden '''
        try:
            serial.write(cmd)
            response=serial.read_until(bytes([0xfd]))
        except Exception as e:
            print(e)
            self.info = e
            return 91 # fehlercodierung , kommt real nicht vor
        serial.close()
        x=  bytes.hex(cmd, ' ').upper()
        #print(f'maxpower={proz}% code= {x}')
        #print('response:',response)
        ok_message = b'\xfe\xfe\xe0\xa4\xfb\xfd'
        ng_message = b'\xfe\xfe\xe0\xa4\xfa\xfd'
        if response == ok_message:
            s=f'maxpower={proz}% eingestellt'
        elif response ==ng_message:
            s=f'***ERROR*** maxpower einstellung : antwort "NotGood" vom ic705'
            self.info = 'Power off via remote'
        else:
            s='unbekannter Fehler'
            self.info = s
        return s

if __name__ =='__main__':
    icom= Icom(port='/dev/ttyACM0', adr= 0xa4, debug=1)
    print(f'Frequenz: {icom.frequenz()}')
    #print(icom.maxpower(100))

