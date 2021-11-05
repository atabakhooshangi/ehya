from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext as _
from rest_framework import exceptions


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise exceptions.ValidationError({'Phone Number': [_('Phone Number is Required.')]})

        user = self.model(
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        if not password:
            raise exceptions.ValidationError({'Password': [_('Password is Required.')]})

        admin = self.create_user(
            phone_number=phone_number
        )

        admin.set_password(password)

        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_admin = True
        admin.save(using=self._db)
        return admin
