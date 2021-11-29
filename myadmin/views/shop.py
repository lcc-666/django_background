from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Shop
from django.core.paginator import Paginator
from datetime import datetime

def index(request,pIndex=1):
    smod=Shop.objects
    mywhere=[]
    slist=smod.filter(status__lt=9)
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status=request.GET.get('status','')
    if status !='':
        slist=slist.filter(status=status)
        mywhere.append('status='+status)

    slist=slist.order_by('id')
    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(slist,5)
    maxpages=page.num_pages
    #判断当前数据页是否越界
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    context={'shoplist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/shop/index.html',context)


def add(request):
    return render(request,'myadmin/shop/add.html')

def insert(request):
    try:
        import time
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        #model实例化
        ob=Shop()
        ob.name=request.POST['name']
        ob.address=request.POST['address']
        ob.phone = request.POST['phone']
        ob.cover_pic=cover_pic
        ob.banner_pic=banner_pic
        ob.status=1
        ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'添加成功! '}
    except Exception as err:
        print(err)
        context = {'info': '添加失败! '}
    return render(request,'myadmin/info.html',context)

def delete(request,sid=0):
    try:
        ob=Shop.objects.get(id=sid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'删除成功! '}
    except Exception as err:
        print(err)
        context = {'info': '删除失败! '}
    return render(request,'myadmin/info.html',context)


def edit(request,sid=0):
    try:
        ob = Shop.objects.get(id=sid)
        context={'shop':ob}
        return render(request, 'myadmin/shop/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的信息!'}
        return render(request, 'myadmin/info.html/', context)

def update(request,sid):
    try:
        ob=Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.status=request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'修改成功! '}
    except Exception as err:
        print(err)
        context = {'info': '修改失败! '}
    return render(request,'myadmin/info.html',context)

