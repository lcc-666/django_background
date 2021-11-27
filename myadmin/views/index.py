from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('欢迎进入点餐系统的后台管理!')