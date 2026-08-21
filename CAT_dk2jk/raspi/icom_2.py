from serial import Serial
from time   import sleep

baudrate = 9600

adr = 0xa4
cmd = [0x03]
pre = [0xFE, 0xFE, adr , 0xE0]
end = [0xFD]

def print_liste_in_hex(l):
        yh=''
        for i in l: # zum drucken
            s= f'{i:02x} '.upper()
            yh=yh+s
        print(yh)
    
def make_request(cmd ):
    # kommando zusammensetzen
    y= pre + cmd + end
    print_liste_in_hex(y)
    request = bytes(y)  # in bytes
    return request

def frequenz( response_ohne_rahmen):
    y= response_ohne_rahmen
    y= y[::-1]   #von hinten nach vorn lesen
    hex_bytes = bytes.hex(y).upper()
    print( hex_bytes)
    mhz = float(hex_bytes)/1e6
    return mhz
  
def cat( cmd = [0x03] ): # liste [commandNr , subcommand, data]
    request = make_request( cmd )
    my_ser   = Serial('/dev/ttyACM0', baudrate)
    my_ser.write(request)  # ascii in bytes umwandeln und senden
    response  = my_ser.read_until(bytes(end))  #echo
    print( bytes.hex(response))
    my_ser.close()
    response_ohne_rahmen= response[5:-1]
    print(response_ohne_rahmen)
    hex_bytes = bytes.hex(response_ohne_rahmen)
    print (hex_bytes)
    return response_ohne_rahmen

def q_f():
    s= ( f'              Frequenz = {frequenz( cat([0x03]) ):.6f} MHz ')
    return s

def q_standby():
    y= cat([0x1a, 0x05,0x00,0x73])
    y1= y[-1:]
    s= bytes.hex(y1)
    b= int(s)
    if b>0:
        s= 'standby'
    else:
        s= 'shutdown'
    s= f'remote control setting = {s}'
    return s

if __name__ == '__main__':
    print( q_f() )    
    #print( q_standby() )
