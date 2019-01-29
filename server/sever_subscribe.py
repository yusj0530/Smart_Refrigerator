import base64
import paho.mqtt.client as mqtt

from main.models import myfind
from mongo.DB import mymongo


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([("tem", 0), ("img", 0)])  # (Topic,QoS)-[("201,0),("101",0)]을 구독한다.


def on_message(client, userdata, msg):

    if str(msg.topic) == "tem":
        pay = msg.payload.decode()
        print("topic: ", str(msg.topic), ",", "pay: ", pay)
        f = myfind("refrigerator", "list")
        print("reDB:", f, type(f))
        for index in f:
            print("index:",index)
            print("a:",index['serial'], type(index['serial']))
            a =index['serial']
            for ref_name in a:

                if ref_name['ref_name']=="ref9":
                    print("ref:",ref_name)
                    print("ref_name:",ref_name['ref_name'])
                    collection = mymongo(ref_name['ref_name'], "temperature")
                    collection.save({"_id": 1, "tem": pay})
                if ref_name['ref_name']=="ref10":
                    print("ref:", ref_name)
                    print("ref_name:", ref_name['ref_name'])
                    collection = mymongo(ref_name['ref_name'], "temperature")
                    collection.save({"_id":1,"tem":-9})
                if ref_name['ref_name']=="ref7":
                    print("ref:", ref_name)
                    print("ref_name:", ref_name['ref_name'])
                    collection = mymongo(ref_name['ref_name'], "temperature")
                    collection.save({"_id":1,"tem":10})
                if ref_name['ref_name']== "ref8":
                    print("ref:", ref_name)
                    print("ref_name:", ref_name['ref_name'])
                    collection = mymongo(ref_name['ref_name'], "temperature")
                    collection.save({"_id": 1, "tem": 40})
     #
     # f = myfind("refrigerator", "list")
     #    print("reDB:", f, type(f))
     #    for index in f:
     #        print("index:", index)
     #        a=index['serial']
     #        print(a, type(a))
     #        serial = index['serial'].keys()
     #        serial_list = list(serial)
     #        print(serial_list)
     #        for i in a:
     #            print(i)
     #            print(i['ref_name'])

    # for index in f:
    #     print("index:", index)
    #     print(index['serial'], type(index['serial']))
    #     serial = index['serial'].keys()
    #     serial_list = list(serial)
    #     print(serial_list)
    #     for i in serial_list:
    #         if i == "ref5":

    if str(msg.topic)=="img":

        f = myfind("refrigerator", "list")
        print("reDB:", f, type(f))
        for index in f:
            print("index:", index)
            a = index['serial']
            print(a, type(a))
            # serial = index['serial'].keys()
            # serial_list = list(serial)
            # print(serial_list)
            for i in a:
                print("i:",i)
                print("r[re]:",i['ref_name'])
                if i['ref_name']=='ref9':
                    collection = mymongo(i['ref_name'], "picture")
                    collection.save({"_id": 2, "img": str(msg.payload)})

                    img_bytes = base64.urlsafe_b64decode(msg.payload)  # .decode('base64')
                    img_path = "C:\\Users\pc\PycharmProjects\practice\statics\images\\ref9.jpg"
                    f = open(img_path, 'wb')  # create a writable Image
                    f.write(img_bytes)
                    print("load")
                    f.close()

                if i['ref_name'] == "ref10":
                    collection = mymongo(i['ref_name'], "picture")
                    collection.save({"_id": 2, "img": str(msg.payload)})

                    img_bytes = base64.urlsafe_b64decode(msg.payload)  # .decode('base64')
                    img_path = "C:\\Users\pc\PycharmProjects\practice\statics\images\\ref10.jpg"
                    f = open(img_path, 'wb')  # create a writable Image
                    f.write(img_bytes)
                    print("load")
                    f.close()

                if i['ref_name'] == "ref7":
                    collection = mymongo(i['ref_name'], "picture")
                    collection.save({"_id": 2, "img": str(msg.payload)})

                    img_bytes = base64.urlsafe_b64decode(msg.payload)  # .decode('base64')
                    img_path = "C:\\Users\pc\PycharmProjects\practice\statics\images\\ref7.jpg"
                    f = open(img_path, 'wb')  # create a writable Image
                    f.write(img_bytes)
                    print("load")
                    f.close()

                if i['ref_name'] == "ref8":
                    collection = mymongo(i['ref_name'], "picture")
                    collection.save({"_id": 2, "img": str(msg.payload)})

                    img_bytes = base64.urlsafe_b64decode(msg.payload)  # .decode('base64')
                    img_path = "C:\\Users\pc\PycharmProjects\practice\statics\images\\ref8.jpg"
                    f = open(img_path, 'wb')  # create a writable Image
                    f.write(img_bytes)
                    print("load")
                    f.close()

client = mqtt.Client()
client.connect("192.168.1.124")


client.on_connect = on_connect
client.on_message = on_message

print("ha")
# member_list()
# refrigerator_list()
client.loop_forever()
