from kxpa import Kxpa

kxpa= Kxpa( port='/dev/ttyUSB0')

# 
# x=kxpa.get_cmd("^SB;")
# print(f'bypass    SWR {x}')        # b'^SB010;' atu bypass swr
# byp_swr=x
# x=kxpa.get_cmd("^SW;")
# print(f'aktuelles SWR {x}')        # tuner swr
# tun_swr=x
# x=kxpa.get_cmd('^PF;')
# print(f'forward   power {x}')
# f_pow=x
# x=kxpa.get_cmd('^PV;')
# print(f'reflected power {x}')
# r_pow=x
# 
# tuner_swr = 1.0001


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
        swr=9.9
    p= get_forward_power()
    if p >10:
        y=f'SWR (KXPA100): {swr}'
    else:
        y=f'SWR (KXPA100): ---'
    return y
    
    
     
print( get_kxpa_swr() )    
    
    