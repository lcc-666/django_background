from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Category,Shop
from django.core.paginator import Paginator
from datetime import datetime

def index(request,pIndex=1):
    umod=Category.objects
    mywhere=[]
    ulist=umod.filter(status__lt=9)
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status=request.GET.get('status','')
    if status !='':
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)
    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,10)
    maxpages=page.num_pages
    #判断当前数据页是否越界
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range

    #遍历当前菜品分类信息并封装对应店铺信息
    for vo in list2:
        sob=Shop.objects.get(id=vo.shop_id)
        vo.shopname=sob.name

    context={'categorylist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/category/index.html',context)


def add(request):
    #获取当前店铺信息
    slist=Shop.objects.values('id','name')
    context={'shoplist':slist}
    return render(request,'myadmin/category/add.html',context)

def insert(request):
    try:
        ob=Category()
        ob.shop_id=request.POST['shop_id']
        ob.name=request.POST['name']
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
    try:
        ob=Category.objects.get(id=uid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'删除成功! '}
    except Exception as err:
        print(err)
        context = {'info': '删除失败! '}
    return render(request,'myadmin/info.html',context)


def edit(request,cid=0):
    try:
        ob = Category.objects.get(id=cid)
        context={'category':ob}
        slist = Shop.objects.values('id', 'name')
        context['shoplist'] = slist
        return render(request, 'myadmin/category/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的信息!'}
        return render(request, 'myadmin/info.html/', context)

def update(request,cid):
    try:
        ob=Category.objects.get(id=cid)
        ob.shop_id=request.POST['shop_id']
        ob.name=request.POST['name']
        ob.status=request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'修改成功! '}
    except Exception as err:
        print(err)
        context = {'info': '修改失败! '}
    return render(request,'myadmin/info.html',context)

