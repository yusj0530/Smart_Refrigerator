from datetime import datetime
import json
import pymongo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

Qt_ref_name = "ref1"
Qt_ref_list = ""
Android_ref_name = "ref1"

@csrf_exempt
def Qt_get_data(request):
    getdata = request.body
    st_data = getdata.decode()
    Qt_data = eval(st_data)
    return Qt_data

@csrf_exempt
def Qt_get_name(request):
    getdata = request.body
    st_data = getdata.decode()
    Qt_data = eval(st_data)
    global Qt_ref_name
    Qt_ref_name = Qt_data['ref_name']
    print("Q:", Qt_ref_name)
    return Qt_ref_name

@csrf_exempt
def list_update(ref,data):
    x = myfind(ref, "list")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[ref]
    print("Qt_data:", data, type(data))
    qtdata = data['list']
    print("qtdata['name']:",qtdata['name'], type(qtdata['name']))
    url = 'http://192.168.1.124:7777/assets/images/' + str(qtdata['name']) + '.jpg'
    tt = datetime.now()
    if len(x) == 0:
        # db에 데이터가 하나도 없을경우 qtdata를 넣어준다.
        keys = qtdata.keys()
        key_list = list(keys)
        for key in key_list:
            db.list.update(
                {'name': qtdata['name']},
                {'$set': {
                    key: qtdata[key], "img": url, "ndate": tt,
                }}, upsert=True)
            print("new data in db:", qtdata['name'])

    else:
        # len(x) != 0: db데이터에 리스트가있다면
        # db데이터의 list하나하나 가져온다.
        for index in x:
            print("db_data:", index, type(index))
            if index['name'] == qtdata['name']:
                # db 리스트의 이름과 qt데이터의 이름이 같다면
                # ["name"]은 banana로 나온다 str
                keys = qtdata.keys()
                key_list = list(keys)
                print("qtdata_amount:", qtdata['amount'])
                if qtdata['amount'] == 0:
                    # qt데이터의 값이 0이라면
                    db.list.delete_one({'name': qtdata['name']})
                    print("delete_qtdata:", qtdata)

                else:
                    # qtdata['amount'] != 0: qt데이터의 값이 0이 아닐 때
                    for key in key_list:
                        db.list.update(
                            {'name': qtdata['name']},
                            {'$set': {
                                key: qtdata[key],"img":url
                            }}, upsert=True)
                        print("update qtdata:",qtdata['name'])
                break
            else:
                print("db_data != qt_data", index['name'])

        else:
            # for~else문 for문이 break없이 쭉 실행되고 else문이 실행된다.
            # index['name'] != qtdata['name']: db에 qtdata가 없을때
            keys = qtdata.keys()
            key_list = list(keys)
            print("qt_key_list:", key_list)
            for key in key_list:
                db.list.update(
                    {'name': qtdata['name']},
                    {'$set': {
                        key: qtdata[key], "img":url, "ndate": tt
                    }}, upsert=True)
                print("input new data: ", qtdata['name'])

@csrf_exempt
def temperature(data):
    x = myfind(data,"temperature")
    tem = x[0]
    print("temperature:", tem, type(tem))
    return json.dumps(tem)

def lday(refname):
    time2 = datetime.now()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[refname]
    f = myfind(refname, "list")
    if "edate" not in f:
        for i in f:
            day = i['ndate']
            yd = day.year
            my = day.month
            dd = day.day
            td = day.hour
            mmd = day.minute
            sd = day.second
            time1 = datetime(yd, my, dd, td, mmd, sd)
            tt = time2-time1
            print(i['name'], "time1:", time1)
            print(i['name'], "tt:", tt)
            print(i['name'], "day:", tt.days)
            db.list.update({"name":i['name']},
                {'$set':{"ldate":tt.days}},upsert=True)

@csrf_exempt
def Qt_Get_list(refname):
    lday(refname)
    get_li = myfind(refname, "list")
    for li in get_li:
        del li['_id']
        del li['ndate']
        if 'edate' in li:
            del li['ldate']
            print("delete ldate")
    dict_li = {'list': get_li}
    print("inventory_list:", dict_li, type(dict_li))
    return json.dumps(dict_li)

@csrf_exempt
def Android_Get_list(refname):
    lday(refname)
    get_li = myfind(refname, "list")
    if get_li == []:
        print("None object")
        x = {"Object":"None"}
        return JsonResponse(x)

    for li in get_li:
        del li['_id']
        del li['ndate']
        if 'edate' in li:
            del li['ldate']
            print("delete ldate")
            print(li)
            dict_li = {'list': get_li}
            return dict_li
    dict_li = {'list': get_li}
    print("inventory_list:", dict_li, type(dict_li))
    return json.dumps(dict_li)

def edate_list(data):
    l = []
    for edate_li in data:
        if 'edate' in edate_li:
            l.append(edate_li)
        print("l", l, type(l))
    return l


def ldate_list(data):
    l = []
    for ldate_li in data:
        if 'edate' not in ldate_li:
            l.append(ldate_li)
        print("l", l, type(l))
    return l

@csrf_exempt
def Android_get_data(request):
    getdata = request.body
    And_data = getdata.decode()
    print("Android_data:", And_data, type(And_data))
    return And_data

@csrf_exempt
def Android_get_name(request):
    getdata = request.body
    And_data = getdata.decode()
    ref_li = And_data.split('&')
    name = ref_li[0]
    ref_name = name[10:]
    print("Android_ref_name:", ref_name)
    global Android_ref_name
    Android_ref_name = ref_name
    return Android_ref_name

@csrf_exempt
def myfind(mydb,mycollection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mydb]
    collection = db[mycollection]
    f = collection.find()
    x = []
    for i in f:
        x.append(i)
    return x