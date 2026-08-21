#!/usr/bin/env python3
#get_serial_ports_v2.py

def get_serial_ports():
    import serial.tools.list_ports as list_ports
    list= list_ports.comports()
    ports=[comport.device for comport in list]
    return ports

def get_all_ports():
    return get_serial_ports()
       
def get_com_ports():
    list_items =get_all_ports()
    com_list_kxpa  = []
    com_list_ic705 = []
    for item in list_items:
        if item.find('USB')>=0:
            com_list_kxpa.append(item)
        else:
            if item.find('ACM')>=0:
                com_list_ic705.append(item)
    
    com_list_kxpa.sort()
    com_list_ic705.sort()
    return com_list_kxpa[0],  com_list_ic705[0] 
            
if __name__ == '__main__':            
    port_kxpa, port_ic705 = get_com_ports()
    print(f' Anschlüsse erkannt :')
    print(f'    KXPA: {port_kxpa}')
    print(f'ICOM_705: {port_ic705}')
    from time import sleep
    sleep(5)  # für display
