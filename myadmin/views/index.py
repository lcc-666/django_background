from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'myadmin/index/index.html')

def login(request):
    return render(request,'myadmin/index/login.html')

def dologin(request):
    pass
def logout(request):
    pass
