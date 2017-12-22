from django import forms
from django.forms import CharField, EmailField
from django.contrib.auth.models import User


class MakeSurePasswordForm(forms.Form):
    password = CharField(required=True, error_messages={'required': '密码不能为空'})
    sure_password = CharField(required=True, error_messages={'required': '请确认密码'})

    def clean_sure_password(self):
        password = self.cleaned_data['password']
        sure_password = self.cleaned_data['sure_password']

        if not password or not sure_password or password != sure_password:
            raise forms.ValidationError('密码填写不匹配')

        return password


class RegisterForm(MakeSurePasswordForm):
    username = CharField(required=True, error_messages={'required': '用户名不能为空'})
    email = EmailField(required=True, error_messages={'required': '请输入正确的邮件格式'})

    def clean_username(self):
        username = self.cleaned_data['username']

        save_user_count = User.objects.filter(username=username).count()
        if save_user_count == 0:
            return username
        elif save_user_count == 1:
            raise forms.ValidationError('用户名已存在')
        else:
            raise forms.ValidationError('用户名异常，请联系管理员核查')


class ForgetPasswordForm(forms.Form):
    username = CharField(required=True, error_messages={'required': '用户名不能为空'})
    email = EmailField(required=True, error_messages={'required': '请输入正确的邮件格式'})

    def clean_username(self):
        username = self.cleaned_data['username']

        save_user_count = User.objects.filter(username=username).count()
        if save_user_count == 0:
            raise forms.ValidationError('用户不存在')
        elif save_user_count == 1:
            return username
        else:
            raise forms.ValidationError('用户名异常，请联系管理员核查')

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'username' not in self.cleaned_data:
            return email

        username = self.cleaned_data['username']

        save_user = User.objects.filter(username=username)
        save_user_count = save_user.count()
        if save_user_count == 0:
            return email
        elif save_user_count == 1:
            if email == save_user[0].email:
                return email
            else:
                raise forms.ValidationError('用户名邮箱不匹配')
        else:
            raise forms.ValidationError('用户名异常，请联系管理员核查')


class ChangePasswordForm(MakeSurePasswordForm):
    username = CharField(required=True, error_messages={'required': '用户名不能为空'})
