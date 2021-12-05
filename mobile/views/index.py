from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member
from datetime import datetime

def index(request):
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
        #print(err)
        #context = {'info': '此账户信息不存在'}
        #return render(request, 'mobile/register.html', context)
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
        request.session['mobileuser'] = member.toDict()
        return redirect(reverse('mobile_index'))
    else:
        context = {'info': '此账户信息禁用或非法'}
        return render(request, 'mobile/register.html', context)

def shop(request):
    return render(request,'mobile/shop.html')

def selectShop(request):
   pass

def addOrders(request):
    return render(request,'mobile/addOrders.html')