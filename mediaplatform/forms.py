from django import forms
from django.forms import CharField

from mediaplatform.models import Contacts


class ContactStatusForm(forms.Form):
    name = CharField(required=True, error_messages={'required': '通讯录姓名不能为空'})
    old_phone_number = CharField(required=True, error_messages={'required': '通讯录旧不能为空'})
    new_phone_number = CharField(required=True, error_messages={'required': '通讯录新号码不能为空'})

    def __init__(self, data, user_id):
        super(ContactStatusForm, self).__init__(data)
        self.user_id = user_id

    def clean_new_phone_number(self):
        old_phone_number = self.cleaned_data['old_phone_number']
        new_phone_number = self.cleaned_data['new_phone_number']
        if old_phone_number == new_phone_number:
            raise forms.ValidationError('新旧号码一样，无需修改')

        name = self.cleaned_data['name']
        contacts = Contacts.objects.filter(user_id=self.user_id, name=name, phone_number=old_phone_number)
        if contacts.count() == 0:
            raise forms.ValidationError('您没有该姓名的通讯录信息')
        elif contacts.count() != 1:
            raise forms.ValidationError('该姓名的通讯录信息不唯一')

        return new_phone_number
