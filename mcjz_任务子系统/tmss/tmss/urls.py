from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('task/', include('task.urls')),

]
