from django.urls import path, re_path
from . import views

app_name = 'mediaplatform'
urlpatterns = [
    path('', views.home, name='home'),
    path('user_info/', views.user_info, name='user_info'),
    re_path('contacts/(?P<user_id>[0-9]+)/', views.contacts, name='contacts'),
]
