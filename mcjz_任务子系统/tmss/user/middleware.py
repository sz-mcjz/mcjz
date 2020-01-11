from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

ALLOW_URL = ['*']


class UserLoginMiddleAware(MiddlewareMixin):
    def process_request(self, request):
        if "/login/" not in request.path:
            uuid = request.COOKIES.get('uuid', None)
            sessionid = request.session.session_key
            if uuid is None:
                return redirect(reverse('login'))
            else:
                pass
        else:
            pass
