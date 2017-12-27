from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def home(request):
    return render(request,
                  'user_info.html')


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def user_info(request):
    return render(request,
                  'user_info.html')
