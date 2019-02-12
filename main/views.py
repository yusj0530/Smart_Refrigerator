from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from main import models
from main.models import myfind, crawling_recipelist, crawling_ingredient
from mongo import update

@csrf_exempt
def Qt_getData(request):
    Qt_data = models.Qt_get_data(request)
    print("Qt_data:", Qt_data, type(Qt_data))
    key = Qt_data.keys()
    key_list = list(key)
    print("qt_key_list:", key_list)
    global Qt_ref_list

    if key_list[0] == "ID":
        # 받아온 qt데이터의 첫번째 키값이 ID일 때
        x = myfind('member', 'list')
        print("member_list:", x, type(x))
        for i in x:
            if i['ID'] == Qt_data['ID'] and i['password'] == Qt_data['Passwd']:
                # 아이디와 비밀번호가 맞다면
                print("correct")
                ref_li = myfind("refrigerator", 'list')
                for i in ref_li:
                    # 냉장고 리스트를 하나씩 가져온다.
                    if i['ID'] == Qt_data['ID']:
                        # qt데이터와 냉장고리스트의 데이터가 ID가 같을 때
                        Qt_ref_list = {'reflist': i['serial']}
                        # 냉장고리스트를 Qt_ref_list변수에 넣는다.
                        print("reflist:",Qt_ref_list)
                        return HttpResponseRedirect("Qt_reflist")
                break
        else:
                print("Not correct")
                Qt_ref_list = {"LoginFail": "ID or password"}
                return HttpResponseRedirect("Qt_reflist")

    if key_list[0] == "list":
        refname = models.Qt_ref_name
        print("Qt_ref_name:",refname)
        update.list_update(refname, Qt_data)
        return HttpResponseRedirect('Qt_list')


# 로그인이 성공했을때 냉장고 리트스 보여주는 함수
@csrf_exempt
def Qt_reflist(request):
    print("Qt_reflist:", Qt_ref_list, type(Qt_ref_list))
    return JsonResponse(Qt_ref_list)

@csrf_exempt
# Qt_get_name변수의 데이터를 넣는다.
def Qt_getRefnum (request):
    models.Qt_get_name(request)
    # Qt_ref_name을 가져온다.
    print("Qt_ref_name:", models.Qt_ref_name)
    print("Response O.K")
    response = {"Response": "O.K"}
    return JsonResponse(response)

@csrf_exempt
def Qt_tem(request):

    if models.Qt_ref_name=="":
        # 냉장고가 선택되지않았을때
        error = {"Response":"Error"}
        return JsonResponse(error)
    # 냉장고가 선택되었을때
    results = models.temperature(models.Qt_ref_name)
    dict_tem = eval(results)
    # 스트링 results을 딕셔너리로 바꾼다.
    # dict_tem = yaml.load(results) eval과 같은 모듈
    del(dict_tem["_id"])
    print("qt_tem", dict_tem, type(dict_tem))
    return JsonResponse(dict_tem)

@csrf_exempt
def Qt_img(request):
    print("Qt_ref_name:", models.Qt_ref_name)
    url = 'http://192.168.1.124:7777/assets/images/'+models.Qt_ref_name+'.jpg'
    pic_results = {"img": url}
    print("Qt_picture:", pic_results, type(pic_results))
    return JsonResponse(pic_results)

@csrf_exempt
def Qt_list(request):
    str_li = models.Qt_Get_list(models.Qt_ref_name)
    # db의 list를 가져온다.
    dict_li = eval(str_li)
    # 딕셔너리로 바꿔준다.
    return JsonResponse(dict_li)

@csrf_exempt
def Qt_ldate(request):
    x = myfind(models.Qt_ref_name,"list")
    str_li = models.ldate_list(x)
    print(str_li, type(str_li))
    li =[]
    for dict_li in str_li:
        del dict_li['_id']
        del dict_li['ndate']
        print(dict_li,type(dict_li))
        li.append(dict_li)
    d = {"list":li}
    print(d,type(d))
    return JsonResponse(d)

@csrf_exempt
def Qt_recipe(request):
    recipelist = crawling_recipelist(request)
    print(recipelist,type(recipelist))
    return JsonResponse(recipelist)

@csrf_exempt
def Qt_ingredient(request):
    material = crawling_ingredient(request)
    print(material,type(material))
    return JsonResponse(material)

@csrf_exempt
def Android_reflist(request):
    And_data = models.Android_get_data(request)
    name = And_data.split('&')
    id = name[0][3:]
    passwd = name[1][5:]
    null = name[2]
    print("ID:", id, "password:", passwd, null)
    if name[0][:2] == "ID":
        x = myfind('member', 'list')
        print("member_list:", x, type(x))
        for i in x:
            if i['ID'] == id and i['password'] == passwd:
                print("correct")
                ref_li = myfind("refrigerator", 'list')
                for i in ref_li:
                    if i['ID'] == id:
                        Android_reflist = {'reflist': i['serial']}
                        print("Android_reflist:", Android_reflist)
                        return JsonResponse(Android_reflist)
                break

        else:
                print("Not correct")
                Not_correct = {"LoginFail": "ID or password"}
                return JsonResponse(Not_correct)

@csrf_exempt 
def Android_getData(request):
    name = models.Android_get_name(request)
    print("Android_ref_name:", name, "Response O.K")
    response = {"Response": "O.K"}
    return JsonResponse(response)

@csrf_exempt
def Android_tem(request):
    # 냉장고가 선택되지않았을때
    if models.Android_ref_name == "":
        error = {"Response":"Error"}
        return JsonResponse(error)
    # 냉장고가 선택되었을때
    results = models.temperature(models.Android_ref_name)
    dict_tem = eval(results)
    del(dict_tem["_id"])
    print("Android_tem:", dict_tem, type(dict_tem))
    return JsonResponse(dict_tem)

@csrf_exempt
def Android_img(request):
    url = 'http://192.168.1.124:7777/assets/images/'+models.Android_ref_name+'.jpg'
    pic_results = {"img": url}
    print("Android_picture:", pic_results, type(pic_results))
    return JsonResponse(pic_results)

@csrf_exempt
def Android_list(request):
    str_li = models.Android_Get_list(models.Android_ref_name)
    dict_li = eval(str_li)
    return JsonResponse(dict_li)

def Android_edate(request):
    x = myfind(models.Android_ref_name, "list")
    str_li = models.edate_list(x)
    if str_li == []:
        print("None object")
        x = {"Object": "None"}
        return JsonResponse(x)
    else:
        li =[]
        for dict_li in str_li:
            del dict_li['_id']
            del dict_li['ndate']
            li.append(dict_li)
        print(li,type(li))
        d = {"list":li}
        print(d,type(d))
        return JsonResponse(d)

@csrf_exempt
def Android_ldate(request):
    # x = myfind("ref4","list")
    x = myfind(models.Android_ref_name,"list")
    str_li = models.ldate_list(x)
    if str_li == []:
        print("None object")
        x = {"Object":"None"}
        return JsonResponse(x)
    else:
        li =[]
        for dict_li in str_li:
            del dict_li['_id']
            del dict_li['ndate']
            li.append(dict_li)
        print(li,type(li))
        d = {"list":li}
        print(d,type(d))
        return JsonResponse(d)