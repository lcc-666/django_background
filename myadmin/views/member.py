from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Member
from django.core.paginator import Paginator
from datetime import datetime

def index(request,pIndex=1):
    umod=Member.objects
    mywhere=[]
    ulist=umod.filter(status__lt=9)
    #获取并判断搜索条件
    kw=request.GET.get('keyword',None)
    status=request.GET.get('status','')
    if status !='':
        ulist=ulist.filter(status=status)
        mywhere.append('status='+status)
    ulist=ulist.order_by('id')
    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,5)
    maxpages=page.num_pages
    #判断当前数据页是否越界
    if pIndex>maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex)
    plist=page.page_range
    context={'memberlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/member/index.html',context)


def delete(request,uid=0):
    try:
        ob=Member.objects.get(id=uid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context={'info':'删除成功! '}
    except Exception as err:
        print(err)
        context = {'info': '删除失败! '}
    return render(request,'myadmin/info.html',context)


