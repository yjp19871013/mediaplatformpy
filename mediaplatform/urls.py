from django.urls import path
from . import views

app_name = 'mediaplatform'
urlpatterns = [
    path('', views.home, name='home'),
    path('user_info/', views.user_info, name='user_info'),
]
