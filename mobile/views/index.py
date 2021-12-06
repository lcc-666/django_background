from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member,Shop,Category,Product
from myadmin.models import Orders,OrderDetail,Payment
from datetime import datetime

def index(request):
    shopinfo= request.session.get('shopinfo',None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))
    clist=Category.objects.filter(shop_id=shopinfo['id'],status=1)
    productlist=dict()
    for vo in clist:
        plist=Product.objects.filter(category_id=vo.id,status=1)
        productlist[vo.id]=plist
    context={'categorylist':clist,'productlist':productlist.items(),'cid':clist[0]}
    return render(request,'mobile/index.html',context)

def register(request):
    return render(request,'mobile/register.html')
def doRegister(request):
    verifycode = '1234'
    if verifycode != request.POST['code']:
        context = {'info': '短信验证码错误!'}
        return render(request, 'mobile/register.html', context)
    try:
        member=Member.objects.get(mobile=request.POST['mobile'])
    except Exception as err:
        ob=Member()
        ob.nickname = '顾客'
        ob.avatar = 'moren.png'
        ob.mobile= request.POST['mobile']
        ob.status=1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        member=ob
    if member.status == 1:
        # 将当前会员信息转成字典格式并存放到session中
        request.session['mobileuser'] = member.toDict()
        # 重定向到登录页
        return redirect(reverse("mobile_index"))
    else:
        context = {"info": '此账户信息禁用！'}
        return render(request, "mobile/register.html", context)


def shop(request):
    context={'shoplist':Shop.objects.filter(status=1)}
    return render(request,'mobile/shop.html',context)

def selectShop(request):
    sid=request.GET['sid']
    ob=Shop.objects.get(id=sid)
    request.session['shopinfo']=ob.toDict()
    request.session['cartlist'] = {}
    return redirect(reverse('mobile_index'))
def addOrders(request):
    cartlist=request.session.get('cartlist',{})
    total_money = 0  # 初始化一个总金额
    # 遍历购物车中的价格进行累加
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']
    request.session['total_money'] = total_money
    return render(request,'mobile/addOrders.html')

def doAddOrders(request):
    try:
        #执行订单信息的添加
        od=Orders()
        od.shop_id=request.session['shopinfo']['id']
        od.member_id=request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status=1
        od.payment_status=2
        od.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        od.save()

        #支付信息添加
        op=Payment()
        op.order_id=od.id
        op.member_id=request.session['mobileuser']['id']
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

    except Exception as err:
        print(err)
    return render(request,'mobile/orderinfo.html',{'order':od})