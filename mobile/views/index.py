from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('欢迎进入会员移动点餐端!')