import paho.mqtt.client as mqtt
from time import time , sleep


### MQTT Items ###################
client = mqtt.Client()
host   = 'raspi62'
port   = 1883

topic = {'pa-freigabe' : 'j', 'polarisation': 'v' } # default, werden von mqtt aktualisiert

class info():
    neu=False
    def set(self):
        self.neu=True
    def get(self):
        x= self.neu
        self.neu= False
        return x
    def __call__(self):
        return self.get()
isInfo= info()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker: {host }")
    print(f"subscribed items: { topic.keys() }")
    for i in list(topic.keys()):
        client.subscribe(i)

def on_message(client, userdata, msg):
    wert=msg.payload.decode()
    msg=msg.topic
    topic[msg] = wert
    print (topic)
    isInfo.set()

def start_client():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 60)
### ende MQTT Items ###################
    
### Main ##############################
pa_freigabe='n'
def run():
    global pa_freigabe
    import random
    t=.33
    start_client()
    client.publish('polarisation-bei-start','v')
    client.publish('pa-freigabe-bei-start' ,'j')
    while True:
        f= random.randrange(1800,444000,100)
        antennen_name= random.choice(['dipol','w3dzz','5-el-beam','vertical','kelemen', 'end-fed'])
        pa_name=random.choice(['2 Watt','1 kW','keine', 'big']) if pa_freigabe=='j' else '---'
        client.loop() # hier wird empfangen und interpretiert
        if isInfo():
            pa_freigabe     =  topic['pa-freigabe']
            ant_polarisation = topic['polarisation']
        client.publish('frequ'  , f )
        client.publish('ant'    , antennen_name  )
        client.publish('pa-name', pa_name )
        sleep(t)
if __name__ =='__main__':
    run()

