import time

class Timer:
    """Verwendung:
obj=Timer( seconds) : Start Instanz
obj()              : timer abgelaufen (boolean)
obj.set(seconds)    : set interval
    """
    def __init__(self, *, sec=1.0):
        self.set(sec)
        
    def set( self,s):
        self._interval = s
        self.en= ( s > 0)
        self.start(time.monotonic())
        
    def start(self,tx):
        self._overflow = tx + self._interval
              
    def __call__( self ):
        now=time.monotonic() 
        if self.en and now > self._overflow:
            self.start(now)
            return True
        else:
            return False
        
       
if __name__== '__main__':
    t= Timer(sec=1.1 )
    n=0
    try:
        while True:
            if t():
                print(n,end=' ') #sec
                n=n+1
    except:
        pass
    finally:
        print('#')
        
        
        
    