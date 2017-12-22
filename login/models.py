from django.contrib.auth.models import User
from django.db import models


class ValidationInfo(models.Model):
    user_id = models.IntegerField(unique=True)
    validation_code = models.CharField(max_length=6)

    @staticmethod
    def save_validation_info(username, validation_code):
        if username:
            save_users = User.objects.filter(username=username)
            if save_users.count() != 1:
                return

            user_id = save_users[0].id

            infos = ValidationInfo.objects.filter(user_id=user_id)
            infos_count = infos.count()
            if infos_count == 0:
                ValidationInfo.objects.create(validation_code=validation_code, user_id=user_id)
            elif infos_count == 1:
                info = infos[0]
                info.validation_code = validation_code
                info.save()
            else:
                raise Exception('数据处理错误')

    def __str__(self):
        return "user_id:" + self.user_id + " validation_code:" + self.validation_code