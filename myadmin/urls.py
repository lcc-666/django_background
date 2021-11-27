from django.urls import path

from myadmin.views import index
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',index.index,name='myadmin_index')
]
