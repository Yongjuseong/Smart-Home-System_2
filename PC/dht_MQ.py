import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

normal_temp = 26.0 # 원하는 온도 설정
MQTT_BROKER = "" # 자신의 raspberry(broker) ip

def on_connect(client,useradta,flags,rc):
    print("Connect with result code"+str(rc))
    client.subscribe("dht/CCL") #Topic

'''
def on_message(client,userdata,msg):
    x=str(msg.payload.decode('utf-8')) #dht 센서 데이터
    print(msg.topic + " " + x)
    if (x != "on" and x != "off"):
        y = eval(x) #dht 센서 데이터를 Dic타입으로 반환 파싱

    if y["temperature"] > normal_temp:
        #publish.single("dht/CCL","on",hostname="192.168.0.15")
        client.publish("dht/CCL","on")

    elif y["temperature"] <=normal_temp:
        #publish.single("dht/CCL","off",hostname="192.168.0.15")
        client.publish("dht/CCL", "off")
'''


def on_message(client, userdata, msg):
    x = str(msg.payload.decode('utf-8'))  # dht 센서 데이터
    print(msg.topic + " " + x)
    if (x != "on" and x != "off"):
        y = eval(x)

        if y["temperature"] > normal_temp:
            publish.single("cmd/CCL", "on", hostname=MQTT_BROKER)

        elif y["temperature"] <= normal_temp:
            publish.single("cmd/CCL", "off", hostname=MQTT_BROKER)

def on_publish(client,userdata,mid):
    print("message publish..")

def on_disconnect(client,userdata,rc):
    print("Disconnected")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER,1883,60)
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.loop_forever()
