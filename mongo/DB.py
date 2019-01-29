
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


# def refrigerator_list():
#     member = myfind("member", "list")
#     print(member, type(member))
#     id = []
#     ref_count = 1
#     serial_count = 1
#     for i in member:
#         id.append(i['ID'])
#     print(id)
#     col = mymongo("refrigerator", "list")
#     for i in id:
#         col.insert({"ID": i, "serial": {"ref" + str(ref_count): "ABCD" + str(serial_count)}})
#         ref_count += 1
#         serial_count += 1

def mymongo(mydb,mycollection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mydb]
    collection = db[mycollection]
    return collection

def insert():
    name = "케첩"
    url = 'http://192.168.1.124:7777/assets/images/'+name+'.jpg'
    tt = datetime.now()
    x = mymongo("ref4","list")
    x.update_one({"name":name},
                 {"$set":{"amount":2,"img":url,"edate":"2021-08-29","ndate":tt}}, upsert=True)
    # x.update_one({"name":name},
    #              {"$set":{"amount":8,"img":url,"ndate":tt}}, upsert=True)
    print(x)
insert()

def test():

    time1 = datetime(2018, 7, 13, 21, 40, 5)
    time2 = datetime.now()
    print(time1)  # 2018-07-13 21:40:05
    print(time2)  # 2018-07-23 20:58:59.666626

    print(time2 - time1)  # 9 days, 23:18:54.666626
    print(type(time2 - time1))  # <class 'datetime.timedelta'>



def lday(refname):
    time2 = datetime.now()
    f = myfind(refname,"list")
    print(f,type(f))
    for i in f:
        print(i,type(i))
        day = i['ndate']
        yd = day.year
        my = day.month
        dd = day.day
        td = day.hour
        mmd = day.minute
        sd = day.second
        time1 = datetime(yd,my,dd,td,mmd,sd)
        print(time1)
        print(time2)
        tt = time2-time1
        print(tt,type(tt))
        print(tt.days)
        return tt.days
        # db.list.update({"name":i['name']},
        #     {'$set':{"ldate":tt.days}},upsert=True)

# lday()