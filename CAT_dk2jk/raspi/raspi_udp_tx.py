import socket
from   time import strftime,gmtime

''' liefert zeit im format "05.Jun.2025 16:24:04 UTC" '''
def get_utc():
    return strftime("%d.%m.%y %H:%M:%S", gmtime())

def send(s):
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    message=s.encode("utf-8")
    sock.sendto(message, (b'127.0.0.1',5000) )
    sock.close

fq=7.032
an='W3DZZ'
pa='KXPA100'
info= '''
-Bei 2m vertical wird die Leistung
 des Ic-705 auf 50% reduziert
-Auf 40m ist IMMER ANT1 (G5RV) gewählt.
'''
ti= get_utc()
message_html=f'''
<pre style="font-size:14px; ">
<hr>
{info}
Time [UTC]: {ti}
System Reboot @ 04:00 h
<p style="font-size: 10px;"><br>Version: 20.Jan.26</p>
</pre>
'''



send(message_html)