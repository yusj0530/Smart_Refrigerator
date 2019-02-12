
from datetime import date
import pymongo
from main.models import myfind
from datetime import datetime, timedelta

def member_list():
    mem_list = mymongo('member', 'list')
    mem_list.insert({"ID": "dbthwjd", "password": "thwjd"})
    mem_list.insert({"ID": "dlcjsdn", "password": "cjsdn"})
    mem_list.insert({"ID": "ghtjdah", "password": "tjdah"})
    mem_list.insert({"ID": "wjddmsgh", "password": "dmsgh"})

def ref_list():
    mem = myfind("refrigerator","list")
    print(mem)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["refrigerator"]
    db.list.update(
        {'ID':'wjddmsgh'},
        {'$set':{
            "serial":[{'ref_name':'ref8','ref_num':'D01'},{'ref_name':'ref9','ref_num':'D02'},{'ref_name':'ref10','ref_num':'D03'}]
        }}, upsert=True)

def mymongo(mydb,mycollection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mydb]
    collection = db[mycollection]
    return collection

def myfind(mydb,mycollection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mydb]
    collection = db[mycollection]
    f = collection.find()
    x = []
    for i in f:
        x.append(i)
    return x
# def DBinsert():
#     name = "우유"
#     url = 'http://192.168.1.124:7777/assets/images/'+name+'.jpg'
#     tt = datetime.now()
#     x = mymongo("ref3","list")
#     x.update_one({"name":name},
#                  {"$set":{"amount":1,"img":url,"edate":"2021-02-25","ndate":tt}}, upsert=True)
#     # x.update_one({"name":name},
#     #              {"$set":{"amount":3,"img":url,"ndate":tt}}, upsert=True)
#     print(x)
# DBinsert()

def update(data,db,url,tt):
    keys = data.keys()
    key_list = list(keys)
    for key in key_list:
        db.list.update(
            {'name': data['name']},
            {'$set': {
                key: data[key], "img": url, "ndate": tt,
            }}, upsert=True)
        print("새로운 물품 업데이트")

def insert(db,data,url,tt):
    db.list.insert({"name": data['name'], "amount": data['amount'],
                    "img": url, "edate": data["edate"], "ndate": tt}, True)
