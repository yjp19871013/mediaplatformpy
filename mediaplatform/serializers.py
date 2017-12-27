from rest_framework import serializers

from mediaplatform.models import Contacts


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('phone_numbers',)
