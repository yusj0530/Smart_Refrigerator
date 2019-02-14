import json
import pymongo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from mongo import DB

RESULT_DIRECTORY = "__result"

Qt_ref_name = "ref6"
Qt_ref_list = ""
Android_ref_name = ""
t = datetime.now()
@csrf_exempt
def Qt_get_data(request):
    # getdata = request.body
    # st_data = getdata.decode()
    # Qt_data = eval(st_data)
    Qt_data = {"list":[{"name":"양파","amount":4,'ndate':'2019-02-13-17-00-00'}]}
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
    db_list = DB.myfind(ref, "list")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[ref]
    qt_data = data['list']
    qtdata = qt_data[0]
    url = 'http://192.168.1.124:7777/assets/images/food/' + str(qtdata['name']) + '.jpg'
    tt = datetime.now()
    if 'ndate' in qtdata:
        qt_ndate = DB.qttime(qtdata)
        qtdata['ndate'] = qt_ndate
    print('qtdate',qtdata)
    qkey = qtdata.keys()
    qt_key = list(qkey)

    if len(db_list) == 0:
        print('len(db_list)==0')
        if 'edate' in qtdata:
            print('edate product update')
            DB.update(qtdata, db, url, tt)
        else:
            print('ldate product update')
            DB.n_update(qtdata, db, url,qtdata['ndate'])
    else:
        print('len(db_list)!=0')
        for dbdata in db_list:
            if qtdata['name']==dbdata['name']:
                print('qt[name]==db[name]')
                if 'edate' in qt_key:
                    print('edate product')
                    if qtdata['amount'] == 0:
                        print('amount==0 and edate product')
                        db.list.delete_one({'name': qtdata['name'], 'edate': qtdata['edate']})
                        print('delete edate product')
                        break
                    else:
                        print('amount!=0 and edate product')
                        if qtdata['edate'] == dbdata['edate']:
                                print('edate product update ')
                                DB.update(qtdata,db,url,tt)
                                break
                        else:
                            print('qt[name]==db[name] and qt[edate]!=db[edate]')
                else:
                    print('ldate product')
                    if qtdata['amount'] == 0:
                        print('amount==0 ldate product')
                        db.list.delete_one({'name': qtdata['name'],'ndate':qtdata['ndate']})
                        break
                    else:
                        print('amount!=0 ldate product')
                        if qtdata['ndate']==dbdata['ndate']:
                            print('qt[ndate]==db[ndate]')
                            print('update ldate product')
                            DB.n_update(qtdata,db,url,qtdata['ndate'])
                            break
                        else:
                            print('qt[name]==db[name] and qt[ndate]!=db[ndate]')
            else:
                print('qt[name]!=db[name]')
        else:
            print('for~else')
            if 'edate' in qtdata:
                print('edate product update')
                DB.update(qtdata,db,url,tt)
            else:
                print('ldate product update')
                DB.n_update(qtdata,db,url,qtdata['ndate'])

@csrf_exempt
def temperature(data):
    x = DB.myfind(data,"temperature")
    tem = x[0]
    print("temperature:", tem, type(tem))
    return json.dumps(tem)

def lday(refname):
    time2 = datetime.now()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[refname]
    db_list = DB.myfind(refname, "list")
    for db_dict in db_list:
        if "edate" not in db_dict:
            day = db_dict['ndate']
            yd = day.year
            md = day.month
            dd = day.day
            hd = day.hour
            mmd = day.minute
            sd = day.second
            time1 = datetime(yd, md, dd, hd, mmd, sd)
            tt = time2-time1
            db.list.update({"name":db_dict['name'],'ndate':db_dict['ndate']},
                    {'$set':{"ldate":tt.days}},upsert=True)
            print('ldate update')

@csrf_exempt
def Qt_Get_list(refname):
    lday(refname)
    get_li = DB.myfind(refname, "list")
    for li in get_li:
        del li['_id']
        day = li['ndate']
        yd = day.year
        md = day.month
        dd = day.day
        hd = day.hour
        mmd = day.minute
        sd = day.second
        tuple_ndate = yd,md,dd,hd,mmd,sd
        s_ndate = str(tuple_ndate)
        ss = s_ndate.replace(', ','-')
        a = ss.strip('(')
        str_ndate = a.strip(')')
        li['ndate']=str_ndate
    print('list:', get_li,type(get_li))
    dict_li = {'list': get_li}
    return json.dumps(dict_li)

@csrf_exempt
def Android_Get_list(refname):
    lday(refname)
    get_li = DB.myfind(refname, "list")
    if get_li == []:
        print("None object")
        x = {"Object":"None"}
        return JsonResponse(x)

    for li in get_li:
        del li['_id']
        del li['ndate']
        if 'edate' and 'ldate' in li:
            del li['ldate']
            print("delete ldate")
            print(li)
            dict_li = {'list': get_li}
            return dict_li
    dict_li = {'list': get_li}
    return json.dumps(dict_li)

def edate_list(data):
    l = []
    for edate_li in data:
        if 'edate' in edate_li:
            l.append(edate_li)
    return l

def ldate_list(data):
    l = []
    for ldate_li in data:
        if 'edate' not in ldate_li:
            l.append(ldate_li)
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

