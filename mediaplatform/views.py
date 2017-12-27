from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
def contacts(request, user_id):
    contacts = Contacts.objects.filter(user_id=user_id)
    if contacts.count() != 1:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = ContactsSerializer(contacts[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

