import smbus
import os
from time import sleep
bus = smbus.SMBus(1)

class PCF8574():
    '''--- PCF8574 Treiber fuer 8-Bit Port Expander -----
Ausgaenge sind low activ !
x=PCF8574(adr= 0x20 )            0x20 default , PCF8574a Adr= 0x48 (**)  
x.clear()                        Alles auf '1' ( Reset)  
x.pin( pinNr{0..7}, value{0|1} ) Pin auf wert setzen
y= x.pin( pinNr{0..7} )          Wert y von Pin lesen
y=x.read()                       Ganzes byte lesen
b=x.read_bin()                   Port binär darstellen b='xxxxxxxx'
x.write( value{0x00.. 0xff} )    Ganzes Byte schreiben
x.event()                        Interrupt an GPIO17 = input geändert
x.input                          Der bei interrupt gelesene wert                                 
(**) pruefe i2c address durch: 'sudo i2cdetect -y -1' im Terminal.
'''  
    def __init__(self,adr= 0x20):    
        self._address=adr
        self.clear()
        self.input=0x00
        file= os.path.realpath(__file__)
        self.__doc__= f'{self.__doc__}Filename :{ file}'
    
    def read(self): 
        try:
            x=bus.read_byte(self._address)
        except Exception as e:
            print (f"error @Address: 0x{self._address:x}")
            print (e)
            x=0xffff
        return x

    def read_bin(self):
        x= self.read()
        b=''
        for i in range(7,-1,-1):
            m= 1<<i
            if x & m :
                b= b+'1'
            else:
                b= b+'0'
        return b

    def write(self,val):
        try:
            bus.write_byte(self._address, int(val))
        except Exception as e:
            print (f"error @Address: {self._address:x}")
            print (e)
        
    def clear(self):
        self.write(0xff)
    
    def _setbit(self,byteValue,bitNr=0,value=1):
        #print(byteValue)
        maske= 1<<bitNr
        x= byteValue
        return x | maske if value else x & ~ maske

    def pin(self,pin,value=None):
        if value== None:  #read     
            return 1 if (self.read() & (1<<pin)) else 0
        else:  #write
            x=self.read()
            y=self._setbit(x,pin,value)
            self.write(y)
    def doc(self):
        pass

def write_doc():    
    doc=f'***** Datei: {__file__}*****\n{PCF8574.__doc__}'
    print(doc)
    with open ('doc_PCF8574.txt', 'w' ) as f:
        f.write(doc)
        
def reset_i2c():
    xout=PCF8574(adr=0x38)
    xin =PCF8574(adr=0x39)
    xout.clear()
    xin.read()

  


    
