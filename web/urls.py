from django.urls import path,include

from web.views import index
urlpatterns = [
    path('',index.index,name='index'),

    #前台登录退出的路由
    path('login', index.login, name='web_login'),
    path('dologin', index.dologin, name='web_dologin'),
    path('logout', index.logout, name='web_logout'),
    path('verify', index.verify, name='web_verify'),

    #为url路由添加请求前缀web/
    path('web/',include([
        path('', index.webindex, name='web_index'),#前台大堂点餐首页
    ]))



]