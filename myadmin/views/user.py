from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

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
    return render(request,'myadmin/user/add.html')

def insert(request):
    try:
        ob=User()
        ob.username=request.POST['username']
        ob.nickname=request.POST['nickname']
        #将当前员工的密码做md5处理
        import hashlib,random
        md5=hashlib.md5()
        n=random.randint(100000,999999)
        s=request.POST['password']+str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash=md5.hexdigest()
        ob.password_salt=n
        ob.status=1
        ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'添加成功! '}
    except Exception as err:
        print(err)
        context = {'info': '添加失败! '}
    return render(request,'myadmin/info.html',context)

def delete(request,uid=0):
    pass

def edit(request,uid=0):
    pass

def update(request,uid):
    pass
