#购物车信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import Product
def add(request):
    # 尝试从session中获取购物车信息
    cartlist = request.session.get("cartlist", {})
    pid = request.GET.get("pid", None)
    if pid is not None:
        product = Product.objects.get(id=pid).toDict()
        product['num'] = 1

        # 判断购物车中是否已存在要购买的商品
        if pid in cartlist:
            cartlist[pid]['num'] += product['num']  # 累加购买量
        else:
            cartlist[pid] = product
        # 将购物车中的商品信息放回到session中
        request.session['cartlist'] = cartlist

    #相应json格式的购物车信息
    return JsonResponse({'cartlist':cartlist})

def delete(request):
    # 尝试从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    #del cartlist[pid]
    # 将cartlist放入session
    request.session['cartlist'] = cartlist
    # 相应json格式的购物车信息
    return JsonResponse({'cartlist': cartlist})

def clear(request):
    request.session['cartlist'] = {}
    # 相应json格式的购物车信息
    return JsonResponse({'cartlist': {}})

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
    # 相应json格式的购物车信息
    return JsonResponse({'cartlist': cartlist})


