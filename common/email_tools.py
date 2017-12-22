import threading

from django.contrib.auth.models import User
from django.core.mail import send_mail

from mediaplatformpy import settings


def send_validate_email_async(username, validation_code):
    if username:
        save_users = User.objects.filter(username=username)
        if save_users.count() != 1:
            return

        t = threading.Thread(target=send_validate_email, args=(save_users[0], validation_code))
        t.setDaemon(True)
        t.start()


def send_validate_email(user, validation_code):
    subject = '密码更改验证码'
    message = user.username + '，' + '您的验证码为：' + validation_code
    send_mail(subject, message, settings.EMAIL_FROM, [user.email])