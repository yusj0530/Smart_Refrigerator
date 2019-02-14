from datetime import datetime

import pymongo

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
            {'name': data['name'],'edate':data['edate']},
            {'$set': {
                key: data[key], "img": url, "ndate": tt,
            }}, upsert=True)
        print("새로운 물품 업데이트")

def n_update(data,db,url,tt):
    keys = data.keys()
    key_list = list(keys)
    for key in key_list:
        db.list.update(
            {'name': data['name'], 'ndate': data['ndate']},
            {'$set': {
                key: data[key], "img": url,'ndate':tt
            }}, upsert=True)
        print("새로운 물품 업데이트")
#
# def einsert(db,data,url,tt):
#     db.list.insert({"name": data['name'], "amount": data['amount'], "img": url, "edate": data["edate"], "ndate": tt}, True)
#
# def linsert(db,data,url,tt):
#     db.list.insert({"name": data['name'], "amount": data['amount'], "img": url, "ndate": tt}, True)

def qttime(data):
    qtime = data['ndate']
    # qtime = '2012-02-22-12-28-00'
    print("Qqqq",qtime,type(qtime))
    a = qtime.split('-')
    print(a,type(a))
    yd = int(a[0])
    my = int(a[1])
    dd = int(a[2])
    td = int(a[3])
    mmd = int(a[4])
    sd = int(a[5])
    qt_ndate = datetime(yd, my, dd, td, mmd, sd)
    print(qt_ndate,type(qt_ndate))
    return qt_ndate
