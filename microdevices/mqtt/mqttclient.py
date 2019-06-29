import paho.mqtt.client as mqtt
import time

class MQTTClient(mqtt.Client):

    def __init__(self, cname, **kwargs):
        super(MQTTClient, self).__init__(cname, **kwargs)
        self.last_pub_time = time.time()
        self.topic_ack = []
        self.run_flag = True
        self.subscribe_flag = False
        self.bad_connection_flag = False
        self.connected_flag = True
        self.disconnect_flag = False
        self.disconnect_time = 0.0
        self.pub_msg_count = 0
        self.devices = []



import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/topic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.17.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

import paho.mqtt.client as mqtt
import paho.mqtt.client as paho

broker="172.17.0.1"
port=1883

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)
#establish connection
ret= client1.publish("test/topic","asd")                   #publish


def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

client1.on_disconnect = on_disconnect
client1.disconnect()
