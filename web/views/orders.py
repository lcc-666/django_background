#订单信息管理试图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator

from myadmin.models import Orders,OrderDetail,Payment,User

def index(request,pIndex=1):
    umod = Orders.objects
    sid=request.session['shopinfo']['id'] #获取当前店铺id号
    mywhere = []
    ulist = umod.filter(shop_id=sid)
    # 获取并判断搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append('status=' + status)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)
    maxpages = page.num_pages
    # 判断当前数据页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    for vo in list2:
        if vo.user_id==0:
            vo.nick='无'
        else:
            user=User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname=user.nickname

    context = {'orderslist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'web/list.html', context)


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
    oid=request.GET.get('oid',0)
    dlist=OrderDetail.objects.filter(order_id=oid)
    context={'detaillist':dlist}
    return render(request,'web/detail.html',context)

def status(request):
    try:
        oid=request.GET.get('oid',0)
        ob=Orders.objects.get(id=oid)
        ob.status=request.GET['status']
        ob.save()
        return HttpResponse('Y')
    except Exception as err:
        print(err)
        return HttpResponse('N')