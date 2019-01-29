import json

import pymongo
from django.db import models

# Create your models here.
def temperature(TOPIC):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["smart_refrigerator"]
    mycol = mydb["temperature"]
    tem = mycol.find({"_id":1})
    pay_tem = tem[0]["tem"]
    # j1 = {"header":TOPIC,"tem":str(pay_tem)}
    j1 = {"header": TOPIC, "tem": pay_tem}
    # print(pay_tem,type(pay_tem))
    # print(j1)
    return json.dumps(j1)