from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.utils import json

from mediaplatform.models import Contacts
from mediaplatform.serializers import ContactsSerializer


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def home(request):
    return render(request,
                  'contacts.html')


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def contacts(request):
    return render(request,
                  'contacts.html')


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def user_info(request):
    return render(request,
                  'user_info.html')


@api_view(['GET'])
def api_contacts_user_details(request, user_id):
    contacts = Contacts.objects.filter(user_id=user_id)
    if contacts.count() == 0:
        ret_dict = {'data': '', 'error': '无此用户'}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    else:
        serializer = ContactsSerializer(contacts, many=True)
        ret_dict = {'data': serializer.data, 'error': ''}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")


@api_view(['POST'])
def api_contacts_update(request):
    serializer = ContactsSerializer(data=request.data, many=True)
    if serializer.is_valid():
        Contacts.objects.all().delete()
        serializer.save()
        ret_dict = {'error': ''}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    else:
        ret_dict = {'error': serializer.errors}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")

