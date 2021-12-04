#订单信息管理试图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime

from myadmin.models import Orders,OrderDetail,Payment

def index(request,pIndex=1):
    pass

def insert(request):
    try:
        #执行订单信息的添加
        od=Orders()
        od.shop_id=request.session['shopinfo']['id']
        od.member_id=0
        od.user_id = request.session['webuser']['id']
        od.money = request.session['total_money']
        od.status=1
        od.payment_status=2
        od.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()

        #支付信息添加
        op=Payment()
        op.order_id=od.id
        op.member_id=0
        op.type=2
        op.bank=request.GET.get('bank',3)
        od.money = request.session['total_money']
        op.status = 2
        op.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        op.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        op.save()

        #执行订单详情的添加
        cartlist=request.session.get('cartlist',{})
        for item in cartlist.values():
            ov=OrderDetail()
            ov.order_id=od.id
            ov.product_id=item['id']
            ov.product_name=item['name']
            ov.price=item['price']
            ov.quantity=item['num']
            ov.status=1
            ov.save()
        del request.session['cartlist']
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse('N')

def detail(request):
    pass

def status(request):
    pass



