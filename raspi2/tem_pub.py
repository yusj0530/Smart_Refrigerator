import paho.mqtt.client as mqtt
TOPIC = "tem"

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.124")
client.loop_start()
client.publish(TOPIC,-8)
client.loop_stop()


