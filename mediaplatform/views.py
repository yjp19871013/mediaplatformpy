from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache
@login_required(login_url='/login/do_login')
def home(request):
    return render(request,
                  'home.html',
                  {'username': request.user.username})
