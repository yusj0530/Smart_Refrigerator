from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from main.models import myfind


def main(request):
    return render(request, 'main.html')

def temperature(request):
    a = myfind("ref1", "temperature")  # 딕셔너리를 포함한 리스트로 나온다
    tem_dict = a[0]['tem']
    response = {'thermometer': tem_dict}

    return JsonResponse(response)
