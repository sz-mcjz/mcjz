from django.urls import path

from user import api

urlpatterns = [
    path('', api.index, name='_index'),
    path('index/', api.index, name='index'),
    path('login/', api.login, name='login'),
    path('profile/', api.profile, name='profile'),
    path('logout/', api.logout, name='logout'),
]
