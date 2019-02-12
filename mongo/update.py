import json
import pymongo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mongo import DB
from mongo.racipe import crawling
from bs4 import BeautifulSoup
from datetime import datetime

RESULT_DIRECTORY = "__result"

Qt_ref_name = "ref1"
Qt_ref_list = ""
Android_ref_name = ""

@csrf_exempt
def Qt_get_data(request):
    # getdata = request.body
    # st_data = getdata.decode()
    # Qt_data = eval(st_data)
    Qt_data = {"list":[{"name":"우유","amount":0,'edate':'2020-05-25'}]}
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
    qt_data = data['list']
    print("qt_data:",qt_data, type(qt_data))
    for qtdata in qt_data:
        url = 'http://192.168.1.124:7777/assets/images/' + str(qtdata['name']) + '.jpg'
        tt = datetime.now()
        if len(x) == 0:
            print('db 데이터가 하나도 없을 경우')
            DB.update(qtdata,db,url,tt)
        else:
            print('len(x)!=0')
            aa=[]
            for index in x:
                aa = index['name']
            if qtdata['name'] not in aa:
                print('물품이 db데이터에 없을 경우')
                print(aa,type(aa))
                DB.update(qtdata, db, url, tt)
                break

            else:
                for index in x:
                    print('물품이 db데이터에 있을 경우')
                    print("db_data:", index, type(index))
                    if index['name'] == qtdata['name']:
                        print('이름이 같다면')
                        if 'edate' in index:
                            print('유통기한이 있다면')
                            if qtdata['edate'] == index['edate']:
                                print('유통기한이 같다면')
                                print("수량은: ", qtdata['amount'])
                                if int(qtdata['amount']) == 0:
                                    print('수량이 0이라면')
                                    db.list.delete_one({'name': qtdata['name']})
                                    print('데이터 삭제')
                                else:
                                    print('수량이 0이 아니라면')
                                    DB.update(qtdata,db,url,tt)
                                    print('qt데이터 업데이트')
                            else:
                                print('유통기한이 다르다면')
                                DB.insert(qtdata, db, url, tt)
                                print('qt데이터 insert')
                        else:
                            print('edate가 없다면 (경과일 물품)')
                            if qtdata['ndate'] == index['ndate']:
                                print('넣은 시간이 같다면')
                                print(qtdata['amount'])
                                if qtdata['amount']== index['amount']:
                                    print('수량이 0이라면')
                                    db.list.delete_one({'name': qtdata['name']})
                                else:
                                    print('수량이 0이 아니라면')
                                    DB.update(qtdata, db, url, qtdata['ndate'])
                                    print('새로운 물품 업데이트')
                            else:
                                print('넣은 시간이 다르다면')
                                DB.insert(qtdata,db,url,qtdata['ndate'])
                                print('새로운 물품 업데이트')

@csrf_exempt
def crawling_recipelist(request):
    results = []
    # 닭볶음탕 레시피
    # qt_name = Qt_get_data
    qt_name = "카레"
    encoding_name = qt_name.encode('utf-8')
    str_name = str(encoding_name)[2:-1]
    name = str_name.replace('\\x', '%')

    # html = crawling('http://www.10000recipe.com/recipe/list.html?q=%EB%8B%AD%EB%B3%B6%EC%9D%8C%ED%83%95&order=accuracy&page=1')
    html = crawling('http://www.10000recipe.com/recipe/list.html?q=%s&order=accuracy&page=1' % name)
    bs = BeautifulSoup(html, 'html.parser')
    tags_div = bs.findAll('div', attrs={'class': 'col-xs-4'})

    print(len(tags_div))

    for tag_div in tags_div:
        # title = tag_div.find('h4', attrs={'class':'ellipsis_title2'}).text
        ex_title = tag_div.find('h4', attrs={'class': 'ellipsis_title2'})
        if ex_title == None:
            print("레시피가 없습니다.")
        else:
            title = ex_title.text
            # ellipsis_title2 레시피 제목
            results.append(title)
        if len(results) == 18:
            break
    print(results, type(results))
    qt_recipe = {'list': results}
    return qt_recipe

@csrf_exempt
def crawling_ingredient(request):
    results = []
    titles = []

    # num =6887142
    # html = crawling("http://www.10000recipe.com/recipe/%d" %num)

    num =6887142
    html = crawling("http://www.10000recipe.com/recipe/%d" %num)

    bs = BeautifulSoup(html, "html.parser")
    tag_div = bs.find("div", attrs={'class':'ready_ingre3'})

    tags_b = tag_div.findAll('b', attrs={'class':'ready_ingre3_tt'})
    for tag_b in tags_b:
        titles.append(tag_b.text)

    tags_li = tag_div.findAll('li')
    tags_span = tag_div.findAll('span', attrs={'class':'ingre_unit'})
    for i in range(0, len(tags_li)):
        ingredient = list(tags_li[i].strings)
        quantity = tags_span[i].text
        results.append((ingredient[0].strip(), quantity))
        # print((ingredient[0].strip(), quantity))
    material = {'material_list':results}
    return material

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
        if 'edate' and 'ldate' in li:
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