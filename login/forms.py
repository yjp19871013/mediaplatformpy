from django import forms
from django.forms import CharField, EmailField


class LoginForm(forms.Form):
    username = CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = CharField(required=True, error_messages={'required': '密码不能为空'})
    email = EmailField(required=True, error_messages={'required': '请输入正确的邮件格式'})
