from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q

def index(request,pIndex=1):
    umod=User.objects
    mywhere=[]
    ulist=umod.filter(status__lt=9)
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
    status=request.GET.get('status','')
    if status !='':
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)




    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,5)
    maxpages=page.num_pages
    #判断当前数据页是否越界
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    context={'userlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/user/index.html',context)


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
