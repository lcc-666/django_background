from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User

def index(request):
    umod=User.objects
    ulist=umod.all()
    context={'userlist':ulist}
    return render(request,'myadmin/user/index.html',context)
    pass

def add(request):
    pass

def insert(request):
    pass

def delete(request,uid=0):
    pass

def edit(request,uid=0):
    pass

def update(request,uid):
    pass
