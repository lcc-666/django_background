from django.urls import path,include

from web.views import index,cart
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
        #购物车信息管理路由
        path('cart/add/<str:pid>', cart.add, name='web_cart_add'),
        path('cart/delete/<str:pid>', cart.delete, name='web_cart_delete'),
        path('cart/clear', cart.clear, name='web_cart_clear'),
        path('cart/change', cart.change, name='web_cart_change'),

    ]))




]