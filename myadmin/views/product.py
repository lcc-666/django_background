from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Category,Shop,Product
import time,os
from django.core.paginator import Paginator
from datetime import datetime

def index(request,pIndex=1):
    umod=Product.objects
    mywhere=[]
    ulist=umod.filter(status__lt=9)
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    cid=request.GET.get('category_id',None)
    if cid:
        ulist = ulist.filter(category_id=cid)
        mywhere.append('category_id='+cid)
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

    #遍历当前菜品分类信息并封装对应店铺和菜品类别信息
    for vo in list2:
        sob=Shop.objects.get(id=vo.shop_id)
        vo.shopname=sob.name
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name

    context={'productlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/product/index.html',context)


def add(request):
    #获取当前店铺信息
    slist=Shop.objects.values('id','name')
    context={'shoplist':slist}
    return render(request,'myadmin/product/add.html',context)

def insert(request):
    try:
        # 图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/product/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        ob=Product()
        ob.shop_id=request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name=request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic=cover_pic
        ob.status=1
        ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'添加成功! '}
    except Exception as err:
        print(err)
        context = {'info': '添加失败! '}
    return render(request,'myadmin/info.html',context)

def delete(request,pid=0):
    try:
        ob=Category.objects.get(id=pid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'删除成功! '}
    except Exception as err:
        print(err)
        context = {'info': '删除失败! '}
    return render(request,'myadmin/info.html',context)


def edit(request,pid=0):
    try:
        ob = Product.objects.get(id=pid)
        context={'product':ob}
        slist = Shop.objects.values('id', 'name')
        context['shoplist'] = slist
        return render(request, 'myadmin/product/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的信息!'}
        return render(request, 'myadmin/info.html/', context)

def update(request,pid):
    '''执行信息编辑'''
    try:
        # 获取原图片
        oldpicname = request.POST['oldpicname']
        # 图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            cover_pic = oldpicname
        else:
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功！"}

        # 判断并删除老图片
        if myfile:
            os.remove("./static/uploads/product/" + oldpicname)

    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}
        # 判断并删除新图片
        if myfile:
            os.remove("./static/uploads/product/" + cover_pic)
    return render(request, "myadmin/info.html", context)

