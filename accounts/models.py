import uuid
from .user_manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission
from django.utils.translation import ugettext as _
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
    permissions = models.ManyToManyField(to=Permission, blank=True, verbose_name=_('دسترسی ها'))

    class Meta:
        verbose_name = _('نقش کاربر')
        verbose_name_plural = _('نقش های کاربری')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def get_role_permissions(self):
        perms_list = []
        perms = self.permissions.all()
        for i in perms:
            val = i.content_type.app_label + '.' + i.codename
            perms_list.append(val)
        return perms_list


# class ProfileCompletionPoints(models.Model):
#     value = models.PositiveIntegerField(default=0, verbose_name=_('مقدار'), null=False, blank=False, help_text=_(
#         'بعد از تکمیل پروفایل این مقدار امتیاز به کاربر توسط کاربر کسب میشود'))
#
#     class Meta:
#         verbose_name = _('امتیاز تکمیل پروفایل  (تنظیمات)')
#         verbose_name_plural = _('امتیاز تکمیل پروفایل (تنظیمات)')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('ایمیل'), max_length=65, unique=True, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('شماره تلفن همراه'), max_length=20, blank=False, null=False,
                                    unique=True)
    role = models.ManyToManyField('Role', verbose_name=_('نقش کاربر'), blank=True)
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

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f' {self.first_name} {self.last_name} - {self.phone_number}'
        return f'{self.phone_number}'

    @property
    def profile_done(self):
        fields = ['first_name', 'last_name', 'province', 'city', 'birthday', 'gender', 'degree', 'field_of_study',
                  'job']
        for field_name in fields:
            if getattr(self, field_name) == "" or None:
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
        if self.points >= AppSettings.objects.last().ticket_cost:
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


# class ActivityPoint(models.Model):
#     value = models.PositiveIntegerField(default=5, verbose_name=_('مقدار'), null=False, blank=False,
#                                         help_text=_('مقدار امتیاز اهدایی جهت استفاده بیش از 5 دقیقه از اپلیکیشن'))
#
#     class Meta:
#         verbose_name = _('امتیاز فعالیت (تنظیمات)')
#         verbose_name_plural = _('امتیاز فعالیت (تنظیمات)')
#
#
# class ReferralPoint(models.Model):
#     value = models.PositiveIntegerField(default=10, verbose_name=_('مقدار'), null=False, blank=False,
#                                         help_text=_('مقدار امتیاز اهدایی جهت دعوت از دوستان'))
#
#     class Meta:
#         verbose_name = _('امتیاز معرفی (تنظیمات)')
#         verbose_name_plural = _('امتیاز معرفی (تنظیمات)')


class AppUpdate(models.Model):
    value = models.BooleanField(default=False, verbose_name=_('دارد'),
                                help_text=_('نشان میدهد آیا اپلیکیشن برروزرسانی دارد یا خیر'))
    link = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('لینک آپدیت'))

    class Meta:
        verbose_name = _('برروزرسانی (تنظیمات)')
        verbose_name_plural = _('برروزرسانی (تنظیمات)')
        ordering = ('value',)

    def __str__(self):
        return self.link


class PointGainHistory(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    action = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('عملیات'))
    point = models.PositiveSmallIntegerField(_('امتیاز'), default=0)
    date_created = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تاریخجه کسب امتیاز')
        verbose_name_plural = _('تاریخجه های کسب امتیاز')
        ordering = ('date_created',)

    def __str__(self):
        return self.user.__str__()


class AppSettings(models.Model):
    ticket_answer_limit = models.PositiveSmallIntegerField(default=6, verbose_name=_('محدودیت تعداد پاسخ تیکت'))
    ticket_cost = models.PositiveSmallIntegerField(default=5, verbose_name=_('هزینه پرسش از طریق تیکت'))
    comment_point = models.PositiveSmallIntegerField(default=1, verbose_name=_('امتیاز ثبت کامنت'))
    support_answer_limit = models.PositiveSmallIntegerField(default=6,
                                                            verbose_name=_('محدودیت تعداد پاسخ تیکت پشتیبانی'))
    profile_completion_point = models.PositiveSmallIntegerField(default=10, verbose_name=_('امتیاز تکمیل پروفایل'))
    activity_point = models.PositiveSmallIntegerField(default=1, verbose_name=_('امتیاز فعالیت'))
    referral_point = models.PositiveSmallIntegerField(default=10, verbose_name=_('امتیاز معرفی دوستان'))

    class Meta:
        verbose_name = _('تنظیمات اپلیکیشن')
        verbose_name_plural = _('تنظیمات اپلیکیشن')
