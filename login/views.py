import json

from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.six import BytesIO
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework import status
from rest_framework.parsers import JSONParser

from common.common_tools import generate_validation_code
from common.email_tools import send_validate_email_async
from login.forms import ForgetPasswordForm, RegisterForm, ChangePasswordForm
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
    username = request.POST.get('username', '')
    if len(username) == 0:
        return redirect(reverse('login:forget_password'))

    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        users = User.objects.get(username=username)
        validation_code = form.cleaned_data['validation_code']
        try:
            info = ValidationInfo.objects.get(user_id=users.id, validation_code=validation_code)
            info.delete()
        except models.DoesNotExist:
            return render(request, 'change_password.html',
                          {'form': form,
                           'username': username},
                          'change_error', '验证码错误，请重新尝试')
        return redirect(reverse('login:do_login'))
    else:
        return render(request, 'change_password.html',
                      {'form': form,
                       'username': username})


@csrf_exempt
@require_POST
def api_login(request):
    data = JSONParser().parse(request)
    username = data.get('username', '')
    password = data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        ret_dict = {'id': user.id, 'username': user.username}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    else:
        ret_dict = {'error': '用户名或密码错误'}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")


@csrf_exempt
@require_POST
def api_logout(request):
    data = JSONParser().parse(request)
    user_id = data.get('id', '')
    username = data.get('username', '')
    if user_id == '' or username == '':
        ret_dict = {'error': 'id或username不能为空'}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")

    user = User.objects.get(pk=user_id)
    if user is None:
        ret_dict = {'error': '无此用户'}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    else:
        if user.username != username:
            ret_dict = {'error': '用户名不匹配'}
            return HttpResponse(json.dumps(ret_dict), content_type="application/json")
        else:
            request.user = user
            logout(request)

            ret_dict = {'id': user.id, 'username': user.username}
            return HttpResponse(json.dumps(ret_dict), content_type="application/json")
