import paho.mqtt.client as mqtt
import base64

TOPIC = "img"
image = 'C:\IoT2018\\card2.jpg'


def on_message(client, userdata, msg):
    # print("", end="")
    print(msg.topic+" "+str(msg.payload))


def getfile(image):
    with open(image, 'rb') as imfile:
        s = str(base64.urlsafe_b64encode(imfile.read()))
        print("%s, %s" % (s, type(s)))
        print(s)
    return s[2:-1]

client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.1.124")
client.loop_start()
img_str = getfile(image)
# jsonobj = json.dumps({"img": img_str})
client.publish(TOPIC, img_str)
client.loop_stop()
