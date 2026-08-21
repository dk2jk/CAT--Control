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
    com_list=[]
    for item in list_items:
        if item.find('USB')>=0:
            com_list.append(item)
        else:
            if item.find('COM')>=0:
                com_list.append(item)
            
    com_list.sort()
    return com_list    
            
if __name__ == '__main__':            
    print(get_com_ports())
    from time import sleep
    sleep(5)  # für display
