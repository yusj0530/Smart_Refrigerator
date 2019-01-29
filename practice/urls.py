"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import main.views as main_views
import web.views as web_views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('main', web_views.main),
    path('main/thermometer', web_views.temperature),

    path('refrigerator/Qt_reflist', main_views.Qt_reflist),
    path('refrigerator/Qt_getData', main_views.Qt_getData),
    path('refrigerator/Qt_getRefnum', main_views.Qt_getRefnum),
    path('refrigerator/Qt_tem', main_views.Qt_tem),
    path('refrigerator/Qt_img', main_views.Qt_img),
    path('refrigerator/Qt_list', main_views.Qt_list),
    path('refrigerator/Qt_ldate', main_views.Qt_ldate),

    path('refrigerator/Android_reflist', main_views.Android_reflist),
    path('refrigerator/Android_getData', main_views.Android_getData),
    path('refrigerator/Android_tem', main_views.Android_tem),
    path('refrigerator/Android_img', main_views.Android_img),
    path('refrigerator/Android_list', main_views.Android_list),
    path('refrigerator/Android_ldate', main_views.Android_ldate),
    path('refrigerator/Android_edate', main_views.Android_edate),

]
