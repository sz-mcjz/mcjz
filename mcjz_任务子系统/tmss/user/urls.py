from django.urls import path

from user import api

urlpatterns = [
    path('', api.login, name='login0'),
    path('login/', api.login, name='login'),
    path('index/', api.index, name='index'),
    path('profile/', api.profile, name='profile'),
    path('logout/', api.logout, name='logout'),
]
