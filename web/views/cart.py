#购物车信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def add(request,pid):
    #从session中获取当前店铺中所有彩屏信息,并从中获取要存放如购物车的菜品
    product=request.session['productlist'][pid]
    product['num']=1 #初始化当前菜品的购买量
    #尝试从session中获取购物车信息
    cartlist=request.session.get('cartlist',{})
    #判断当前购物车中是否存在要放进购物车的菜品
    if pid in cartlist:
        cartlist[pid]['num']+=product['num']
    else:
        cartlist[pid]=product
    #将cartlist放入购物车
    request.session['cartlist']=cartlist
    #print(cartlist)
    #跳转到点餐首页
    return redirect(reverse('web_index'))

def delete(request,pid):
    # 尝试从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    # 将cartlist放入session
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))

def clear(request):
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))

def change(request):
    # 尝试从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    pid=request.GET.get('pid',0)#获取要修改的菜品id
    m=int(request.GET.get('num',1))#要修改的数量
    if m<1:
        m=1
    cartlist[pid]['num']=m  #修改购物车的数量
    # 将cartlist放入session
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))


