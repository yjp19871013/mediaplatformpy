from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache


@never_cache
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
def do_logout(request):
    logout(request)
    return render(request, 'login.html')
