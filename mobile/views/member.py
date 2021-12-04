from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    return HttpResponse('欢迎进入会员移动点餐端!')