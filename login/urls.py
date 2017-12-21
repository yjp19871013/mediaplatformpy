from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('do_login/', views.do_login, name='do_login'),
    path('logout/', views.do_logout, name='do_logout'),
]
