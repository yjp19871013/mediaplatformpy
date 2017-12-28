from django.contrib.auth.models import User
from django.db import models


class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=50, null=False)
