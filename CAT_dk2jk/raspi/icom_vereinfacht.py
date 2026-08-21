from serial import Serial

def icom_frequenz(port='/dev/ttyACM0'):
        hexKommando   = "FE FE A4 E0 03 FD"   #space ignored
        bytesKommando = bytes.fromhex(hexKommando)  # b'\xfe\xfe\xa4\xe0\x03\xfd'
        
        serial = Serial( port, baudrate=9600, timeout=1, writeTimeout=1) 
        serial.write(bytesKommando)     
        antwort = serial.read_until(bytes([0xfd]))
                                        # b'\xfe\xfe\xe0\xa4\x03\x00P\x878\x04\xfd'          
        serial.close() 
        hexString=bytes.hex(antwort)    # 'fefee0a4030050873804fd'
                                        #  0123456789012345678901  <<- index
        s=''
        for i in range(18,9,-2):        # 0050873804 von hinten nach vorne 
                                        # lesen in 2er- Päckchen
            s = s+hexString[i:i+2]      #  => '0438875000'
        x1  = int(s)     # 438875000    # führende Nullen entfernen und in Ganzzahl umwandeln
        khz = x1//1000    # 438875      # integer division => khz
        return khz  #  [kHz]:           # 438875

fq=icom_frequenz(port='/dev/ttyACM0')
print(f'Frequenz: {fq}')


