from django.urls import path, re_path
from . import views

app_name = 'mediaplatform'
urlpatterns = [
    path('', views.home, name='home'),
    path('contacts', views.contacts, name='contacts'),
    path('user_info/', views.user_info, name='user_info'),
    path('modify_phone_number/', views.modify_phone_number, name='modify_phone_number'),
    path('delete_phone_number/', views.delete_phone_number, name='delete_phone_number'),
    path('api_contacts_update/', views.api_contacts_update, name='api_contacts_update'),
    re_path('api_contacts_user_details/(?P<user_id>[0-9]+)/',
            views.api_contacts_user_details, name='api_contacts_user_details'),
    re_path('api_contacts_operation/(?P<user_id>[0-9]+)/',
            views.api_contacts_operation, name='api_contacts_operation'),
]
