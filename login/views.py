from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from login.forms import LoginForm


@never_cache
@require_http_methods(["GET", "POST"])
def do_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('mediaplatform:home'))
    else:
        return render(request, 'login.html', {
            'username': username,
            'login_error': "用户名或密码错误"
        })


@never_cache
@require_POST
def do_logout(request):
    logout(request)
    return render(request, 'login.html')


@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    form = LoginForm(request.POST)
    if form.is_valid():
        return render(reverse('login:do_login'))
    else:
        print(form.errors)
        return render(request, 'register.html', {'errors': form.errors})


@never_cache
@require_http_methods(["GET", "POST"])
def forget_password(request):
    pass
