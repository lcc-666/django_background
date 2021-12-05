from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    return render(request,'mobile/member.html')
def orders(request):
    return render(request,'mobile/member_orders.html')
def detail(request):
    return render(request,'mobile/member_detail.html')
def logout(request):
    del request.session['mobileuser']
    return render(request,'mobile/register.html')
