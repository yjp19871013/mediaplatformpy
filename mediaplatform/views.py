from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
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
    return redirect(reverse('mediaplatform:contacts'))


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def contacts(request):
    search_name = request.GET.get('search_name', '')

    if len(search_name) == 0:
        contacts_objects = Contacts.objects.all()
    else:
        contacts_objects = Contacts.objects.filter(name=search_name)

    show_contacts = {}
    for contact in contacts_objects:
        name = contact.name
        if name in show_contacts:
            phone_numbers = show_contacts[name]
            phone_numbers.append(contact.phone_number)
            show_contacts[name] = phone_numbers
        else:
            show_contacts.setdefault(name, [contact.phone_number])

    return render(request,
                  'contacts.html',
                  {'show_contacts': show_contacts,
                   'search_name': search_name})


@never_cache
@login_required(login_url='/mediaplatform_login/do_login')
@require_GET
def user_info(request):
    return render(request,
                  'user_info.html')


@api_view(['GET'])
def api_contacts_user_details(request, user_id):
    contacts_objects = Contacts.objects.filter(user_id=user_id)
    if contacts_objects.count() == 0:
        ret_dict = {'data': [], 'error': ''}
        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    else:
        serializer = ContactsSerializer(contacts_objects, many=True)
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

