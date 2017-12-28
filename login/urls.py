from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('do_login/', views.do_login, name='do_login'),
    path('do_logout/', views.do_logout, name='do_logout'),
    path('register/', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('api_login/', views.api_login, name='api_login'),
    path('api_logout/', views.api_logout, name='api_logout')
]
