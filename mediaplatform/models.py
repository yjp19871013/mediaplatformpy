from django.contrib.auth.models import User
from django.db import models


class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_numbers = models.CharField(max_length=255, null=False)

