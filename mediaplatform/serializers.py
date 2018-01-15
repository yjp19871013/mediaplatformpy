from django.contrib.auth.models import User
from rest_framework import serializers

from mediaplatform.models import Contacts, ContactsOperation


class ContactsSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(max_length=50, allow_null=False)

    def validate(self, attrs):
        if 'user_id' in attrs:
            user_id = attrs['user_id']
            users = User.objects.filter(pk=user_id)
            if users.count() == 0:
                raise serializers.ValidationError('该用户不存在')
            elif users.count() != 1:
                raise serializers.ValidationError('用户数据错误')
            else:
                return attrs
        else:
            raise serializers.ValidationError('缺少user_id字段')

    def update(self, instance, validated_data):
        user_id = validated_data.get('user_id', instance.user_id)
        users = User.objects.get(pk=user_id)
        instance.user_id = users[0]
        return instance

    class Meta:
        model = Contacts
        fields = ('id', 'user_id', 'name', 'phone_number',)


class ContactsOperationSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer(read_only=True)

    class Meta:
        model = ContactsOperation
        fields = ('id', 'user_id', 'operation', 'new_phone_number', 'new_name', 'contacts',)
