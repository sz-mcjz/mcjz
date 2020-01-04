from django.urls import path

from user import api

urlpatterns = [
    path('login/', api.login, name='login'),
    path('index/', api.index, name='index'),
    path('profile/', api.profile, name='pim'),
    path('logout/', api.logout, name='logout'),
]
