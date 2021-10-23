import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext as _

from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

GENDER_CHOICES = (
    ('مرد', 'مرد'),
    ('زن', 'زن'),
)

ROLE_CHOICES = (
    ('1', 'عضو عادی'),
    ('2', 'عضو فعال'),
    ('3', 'کارشناس'),
    ('4', 'کارشناس ارشد'),
    ('5', 'مدیر'),
    ('6', 'مدیر ارشد'),
    ('7', 'دانشجو'),
    ('8', 'استاد'),
    ('9', 'حکیم'),
    ('10', 'عضو جامعه'),
    ('11', 'شورای مرکزی'),
    ('12', 'مراجعین مطب'),
    ('13', 'مدیر کل'),
)


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


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('ایمیل'), max_length=65, unique=True, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('شماره تلفن همراه'), max_length=20, blank=False, null=False,
                                    unique=True)
    role = models.CharField(verbose_name=_('نوع عضویت'), max_length=20, choices=ROLE_CHOICES, default=1)
    first_name = models.CharField(verbose_name=_('نام'), max_length=75, null=True, blank=True)
    last_name = models.CharField(verbose_name=_('نام خانوادگی'), max_length=75, null=True, blank=True)
    province = models.CharField(verbose_name=_('استان'), max_length=40, null=True, blank=True)
    city = models.CharField(verbose_name=_('شهر'), max_length=40, null=True, blank=True)
    birthday = models.CharField(verbose_name=_('تاریخ تولد'), max_length=10, null=True, blank=True)
    gender = models.CharField(verbose_name=_('جنسیت'), choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    degree = models.CharField(verbose_name=_('مدرک تحصیلی'), max_length=30, null=True, blank=True)
    field_of_study = models.CharField(verbose_name=_('رشته تحصیلی'), max_length=60, null=True, blank=True)
    job = models.CharField(verbose_name=_('شغل'), max_length=60, null=True, blank=True)
    referral = models.ForeignKey('User', verbose_name=_('معرف'), related_name='ref', null=True, blank=True,
                                 on_delete=models.CASCADE)
    user_referrals = models.ManyToManyField('User', verbose_name=_('معرفی کرده'), related_name='urefs', blank=True)
    points = models.IntegerField(verbose_name=_('امتیاز'), default=0)
    ip = models.CharField(verbose_name=_('آدرس آی پی'), max_length=15, blank=True, null=True)
    verify_code = models.IntegerField(verbose_name=_('کد احراز'), default=0, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name=_('آخرین بازدید'), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_('تاریخ عضویت'), auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        data = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return data

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربرها')
        ordering = ('date_joined',)
