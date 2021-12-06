from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member,Shop,Orders,OrderDetail,Payment,User


def index(request):
    return render(request,'mobile/member.html')


def orders(request):
    mod = Orders.objects
    mid = request.session['mobileuser']['id']  # 获取当前店铺id号
    olist=mod.filter(member_id=mid)
    # 获取并判断搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
    list2=olist.order_by('-id')
    orders_status=['无','排队中','已撤销','已完成']
    for vo in list2:
        plist=OrderDetail.objects.filter(order_id=vo.id)[:4]
        vo.plist=plist
        vo.statusinfo=orders_status[vo.status]

    context = {'orderslist': list2}
    return render(request, 'mobile/member_orders.html', context)
def detail(request):
    pid=request.GET.get('pid',0)
    order=Orders.objects.get(id=pid)
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop=Shop.objects.only('name').get(id=order.shop_id)
    order.shopname=shop.name
    orders_status = ['无', '排队中', '已撤销', '已完成']
    order.statusinfo = orders_status[order.status]
    return render(request,'mobile/member_detail.html',{'order':order})
def logout(request):
    del request.session['mobileuser']
    return render(request,'mobile/register.html')
