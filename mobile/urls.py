from django.urls import path

from mobile.views import index,member
urlpatterns = [
    path('',index.index,name='moblie_index'),

    path('register',index.register,name='moblie_register'),
    path('doregister',index.doRegister,name='moblie_doregister'),
    path('shop',index.shop,name='moblie_shop'),
    path('shop/select',index.selectShop,name='moblie_selectShop'),
    path('orders/add',index.addOrders,name='moblie_addOrders'),

    path('member',member.index,name='moblie_member_index'),
    path('member/orders',member.orders,name='moblie_member_orders'),
    path('member/detail',member.detail,name='moblie_member_detail'),
    path('member/logout',member.logout,name='moblie_member_logout'),

]