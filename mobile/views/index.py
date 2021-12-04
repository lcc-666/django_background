from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    return render(request,'mobile/index.html')
def register(request):
    return render(request,'mobile/register.html')
def doRegister(request):
    #return render(request,'mobile')
    pass
def shop(request):
    return render(request,'mobile/shop.html')
def selectShop(request):
   # return render(request,'mobile')
    pass

def addOrders(request):
    return render(request,'mobile/addOrders.html')