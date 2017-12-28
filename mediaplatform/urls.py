from django.urls import path, re_path
from . import views

app_name = 'mediaplatform'
urlpatterns = [
    path('', views.home, name='home'),
    path('user_info/', views.user_info, name='user_info'),
    path('api_contacts_update/', views.contacts_update, name='contacts_update'),
    re_path('api_contacts_user_details/(?P<user_id>[0-9]+)/', views.contacts_user_details, name='contacts_user_details'),
]
