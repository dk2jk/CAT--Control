import re
import serial

adr         = "58"  # "58" ... ic-706 , ( "A4" ... ic-705 )
cmd_write_f = "00"
cmd_read_f  = "03"
end         = "FD"
port        = "/dev/ttyUSB2"
baud        = 9600
cat = serial.Serial(port, baud , timeout=1, writeTimeout=2)

def write_f( f=7.123456):
    print(f'          Sollfrequenz: {f} MHz')
    f= int(f*1e6)
    s= f'{f:010d}' # "0007123456" format 10 zeichen mit nullen
    print(f" Formatiert mit Nullen: '{s}'")
    list_hex = (re.findall(r'.{2}', s))
    # ['56', '34', '12', '07', '00']
    print(f'split zu 2-er Gruppen: {list_hex}')
    list_hex=list_hex[::-1]
    print(f'             gewendet: {list_hex}')
    f_data=''
    for i in list_hex:
        f_data= f_data + i
        # 5634120700
    print (f"                zusammengefügt :'{f_data}'")
    
    cmd_hex="FEFE" + adr + "E0" + cmd_write_f + f_data + end
    # FEFE58E0005634120700FD
    print(f"komplettes Kommando : '{cmd_hex}'")
    b =  bytes.fromhex(cmd_hex)
    # b'\xfe\xfeX\xe0\x00V4\x12\x07\x00\xfd'
    print(f"      gesendet in Bytes: {b}")
    cat.write(b)
    dummy = cat.read_until(expected=b'\xfd') # echo
    y= cat.read_until(expected=b'\xfd')      # antwort
    print(f'es kommt nichts zurück : {y}') # b'' 
    
def read_f():
    cmd_hex= "FE FE "+ adr + " E0 "+ cmd_read_f+ " " + end
    print(f"ICOM Kommando (hex): '{cmd_hex}'")
    b =  bytes.fromhex(cmd_hex)
    #print(f'Kommando als Bytes: {b}')
    cat.write(b)
    dummy = cat.read_until(expected=b'\xfd') # echo
    y= cat.read_until(expected=b'\xfd')      # antwort
    #print(f'  Antwort in Bytes: {y}')
    s= y.hex() 	
    print(f"    Antwort in Hex: '{s}'  => Text")
    list_hex = (re.findall(r'.{2}', s))
    print('aufgesplittet in 2-er Gruppen:')
    print(f'{list_hex}')
    data= list_hex[5:10]
    print (f'Nutzdaten ...                 {data} ')
    data1= data[::-1]
    print(f'von hinten gelesen...         {data1}')
    f1=''
    for i in data1:
         f1= f1+i
    print(f"zusammengefügt:                '{f1}'  = f1")
    f= int(f1)/1e6	# 7.123456
    print (f'Ergebnis      = {f} MHz  ... f = int(f1)/1e6')
    return f
        

