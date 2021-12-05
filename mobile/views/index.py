from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member,Shop
from datetime import datetime

def index(request):
    shopinfo= request.session.get('shopinfo',None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))
    return render(request,'mobile/index.html')
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
    return redirect(reverse('mobile_index'))
def addOrders(request):
    return render(request,'mobile/addOrders.html')