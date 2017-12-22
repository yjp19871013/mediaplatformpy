from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from common.common_tools import generate_validation_code
from common.email_tools import send_validate_email_async
from login.forms import ForgetPasswordForm, RegisterForm
from login.models import ValidationInfo


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
    return redirect(reverse('login:do_login'))


@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    form = RegisterForm(request.POST)
    if form.is_valid():
        User.objects.create_user(form.cleaned_data['username'],
                                 form.cleaned_data['email'],
                                 form.cleaned_data['password'])
        return redirect(reverse('login:do_login'))
    else:
        return render(request, 'register.html', {'form': form})


@never_cache
@require_http_methods(["GET", "POST"])
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'forget_password.html')

    form = ForgetPasswordForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        validation_code = generate_validation_code()
        #send_validate_email_async(username, validation_code)
        ValidationInfo.save_validation_info(username, validation_code)
        return render(request, 'change_password.html', {'username': username})
    else:
        return render(request, 'forget_password.html', {'form': form})


@never_cache
@require_POST
def change_password(request):
    pass


