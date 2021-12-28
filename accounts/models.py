import uuid
from .user_manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext as _
from ticket.models import TicketPointCost
from rest_framework_simplejwt.tokens import RefreshToken

GENDER_CHOICES = (
    ('مرد', 'مرد'),
    ('زن', 'زن'),
)

PROFILE_POINT_CHOICES = (
    ('1', 'کسب شده'),
    ('2', 'کسب نشده'),
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
    ('14', 'مدیر مطب'),
    ('15', 'مدیر ارشد مطب'),
    ('16', 'مدیر سایت'),
    ('17', 'مدیر ارشد سایت'),
    ('18', 'مدیر اپلیکیشن'),
    ('19', 'مدیر ارشد اپلیکیشن'),
    ('20', 'مدیر روابط عمومی'),
    ('21', 'مدیر ارشد روابط عمومی'),
    ('22', 'مدیر آموزش'),
    ('23', 'مدیر ارشد آموزش'),
)


class Role(models.Model):
    name = models.CharField(_('نام نقش'), max_length=50, null=False, blank=False)
    is_expert = models.BooleanField(_('ارشد'), default=False)

    class Meta:
        verbose_name = _('نقش کاربر')
        verbose_name_plural = _('نقش های کاربری')
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProfileCompletionPoints(models.Model):
    value = models.PositiveIntegerField(default=0, verbose_name=_('مقدار'), null=False, blank=False, help_text=_(
        'بعد از تکمیل پروفایل این مقدار امتیاز به کاربر توسط کاربر کسب میشود'))

    class Meta:
        verbose_name = _('امتیاز اولبه')
        verbose_name_plural = _('امتیاز اولبه')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('ایمیل'), max_length=65, unique=True, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('شماره تلفن همراه'), max_length=20, blank=False, null=False,
                                    unique=True)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, verbose_name=_('نقش کاربر'), null=True, blank=True)
    first_name = models.CharField(verbose_name=_('نام'), max_length=75, null=True, blank=True, default="")
    last_name = models.CharField(verbose_name=_('نام خانوادگی'), max_length=75, null=True, blank=True, default="")
    province = models.CharField(verbose_name=_('استان'), max_length=40, null=True, blank=True, default="")
    city = models.CharField(verbose_name=_('شهر'), max_length=40, null=True, blank=True, default="")
    birthday = models.CharField(verbose_name=_('تاریخ تولد'), max_length=10, null=True, blank=True, default="")
    gender = models.CharField(verbose_name=_('جنسیت'), choices=GENDER_CHOICES, max_length=10, null=True, blank=True,
                              default="")
    degree = models.CharField(verbose_name=_('مدرک تحصیلی'), max_length=30, null=True, blank=True, default="")
    field_of_study = models.CharField(verbose_name=_('رشته تحصیلی'), max_length=60, null=True, blank=True, default="")
    job = models.CharField(verbose_name=_('شغل'), max_length=60, null=True, blank=True, default="")
    referral = models.ForeignKey('User', verbose_name=_('معرف'), related_name='ref', null=True, blank=True,
                                 on_delete=models.CASCADE)
    user_referrals = models.ManyToManyField('User', verbose_name=_('معرفی کرده'), related_name='urefs', blank=True)
    points = models.IntegerField(verbose_name=_('امتیاز'), default=0)
    profile_completion_point = models.CharField(_('امتیاز تکمیل پروفایل'), max_length=1, choices=PROFILE_POINT_CHOICES,
                                                default='2')
    ip = models.CharField(verbose_name=_('آدرس آی پی'), max_length=15, blank=True, null=True)
    verify_code = models.IntegerField(verbose_name=_('کد احراز'), default=0, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name=_('آخرین بازدید'), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_('تاریخ عضویت'), auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False, verbose_name=_('تیم پشتیبانی'))

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return f' کاربر  {self.role} - {self.phone_number}'

    @property
    def profile_done(self):
        fields = ['first_name', 'last_name', 'province', 'city', 'birthday', 'gender', 'degree', 'field_of_study',
                  'job']
        for field_name in fields:
            if getattr(self, field_name) is "" or None:
                return False
        return True

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        data = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return data

    @property
    def check_point_status_for_ticket(self):
        if self.points >= TicketPointCost.objects.last().value:
            return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربرها')
        ordering = ('date_joined',)
