# berechnungen


tabelleAfu= [\
[ 1.810000  , 1.999999, '160m'],
[ 3.500000  , 3.800000, '80m'],
[ 5.255000  , 5.405000, '60m'],
[ 7.000000  , 7.200000, '40m'],
[ 10.100000 , 10.150000,'30m'],
[ 14.000000 , 14.350000,'20m'],
[ 18.068000 , 18.168000,'17m'],
[ 21.000000 , 21.450000,'15m'],
[ 24.890000 , 24.990000,'12m'],
[ 28.000000 , 29.700000,'10m'],
[ 50.000000 , 52.000000,'6m',],
[ 144.000000, 146.000000,'2m'],
[ 430.000000, 440.000000,'70cm'],
]

''' ein bit in byte auf value setzen '''
def setbit(byte, bitnr,value = None):   
    if value == None:  #read
        return 1 if (byte & (1 << bitnr)) else 0
    else:              #write
        maske = 1 << bitnr
        byte  = byte | maske if value else byte  & ~ maske
        return byte


''' liefert den index aus tabelleAfu für mhz'''  
def afu_band_nr(mhz):
    index=-1
    x = tabelleAfu
    n= len(tabelleAfu)
    for zeile in range (n):
        funten = x[zeile][0]
        foben  = x[zeile][1]
        if mhz >= funten and mhz < foben:
            index=zeile
            break
    return index

''' grobe unterteilung in frequenzbereiche '''
def bereich(f):
    
    if f > 200:
        name= 'uhf'
    elif f >100:
        name= 'vhf'
    else:    #f <=100
        name=  'kw'
    return name

''' antenne nummer  je nach bereich und polarisation '''
def ant_nr( bereich, pol='v'):
    if bereich =='kw':
        antNr=1
        #unabhaengig von pol.
    elif bereich =='vhf': # 2m
        # antNr 2 oder 3
        if pol=='h': # horizontal
            antNr=2 # 2 ist horizontal
        else: # vertikal
            # antNr=3 # 3 ist vertikal
            antNr=3 
    elif bereich=='uhf':
        if pol =='h':
            antNr=4      # 5 (70cm) horizontal im moment nicht vorhanden
        else:
            antNr=4
    else:
        antNr=0
    return antNr

''' liefert relais-bitmuster (k3,k2,k1) in abhaengigkeit von antennen nummer '''
def relais_bits(antNr):
    if antNr==3:
        rel=(1,0,0) # k3,k2,k1      
    elif antNr==5:
        rel=(0,1,1) # k3,k2,k1  
    else:   # antNr ==1,2,4:
        rel=(1,1,1) # k3,k2,k1
    return rel

''' liefert ptt-bitmuster (enpa2n,70,2m,kw) '''
''' in abhaengigkeit von band nummer und pa freigabe '''
def ptt_bits(bandNr, pa_enable):
    ruhezustand = (1,1,1,1) 
    if bandNr < 0 :
        # kein afu band
        ptt= ruhezustand  # enpa2n,70,2m,kw
    else:
        if bandNr <= 10: # kw  
            if pa_enable:
                ptt= (1,1,1,0)  # enpa2n,70,2m,kw
            else:
                ptt= ruhezustand  # enpa2n,70,2m,kw
        elif bandNr == 11:      # vhf / 2m
            if pa_enable:
                ptt= (0,1,0,1)  # enpa2n,70,2m,kw
            else:
                ptt= ruhezustand  # enpa2n,70,2m,kw
        elif bandNr == 12:  # uhf/ 70cm 
            if pa_enable:
                ptt= (1,0,1,1)  # enpa2n,70,2m,kw
            else:
                ptt=ruhezustand  # enpa2n,70,2m,kw
        else:   # d.c.
            ptt= ruhezustand  # enpa2n,70,2m,kw
    return ptt
    
''' voreinstellung der relais '''
def preset(ptt,rel):
    y= 0xff
    y=setbit(y,0,ptt[0]) # paen 2m
    y=setbit(y,3,ptt[1]) # ptt kw
    y=setbit(y,2,ptt[2]) # ptt 2m
    y=setbit(y,1,ptt[3]) # ptt 70cm
    y=setbit(y,6,rel[0]) # k1
    y=setbit(y,5,rel[1]) # k2
    y=setbit(y,4,rel[2]) # k3
    y=setbit(y,7,1)      # k4
    return y
 
''' die Ausgangs sollwerte anschaulich darstellen 0 = 'ein' '''
''' ['k4', 'k3', 'k2', 'k1', '70', '2m', 'kw', 'en']        '''
''' [' 1', ' 1', ' 1', ' 1', ' 1', ' 1', ' 1', ' 1']        '''
def display_port(x):
    y=['--']*8
    z= ['k4', 'k3', 'k2', 'k1', '70', '2m', 'kw', 'en']
    for i in range(8):
        maske=1<<i
        y[i]=' 1' if (x & maske) > 0 else ' 0'
    y.reverse()
    print(z)
    print(y)       

