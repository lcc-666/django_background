from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('ShopMiddleware')
        # One-time configuration and initialization.

    def __call__(self, request):
        path=request.path
        print('url',path)

        urllist=['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']

        if re.match(r'^/myadmin',path) and (path not in urllist):
            if 'adminuser' not in request.session:
                return redirect(reverse('myadmin_login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response