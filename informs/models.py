from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from accounts.models import Role

User = get_user_model()

TYPE_CHOICES = (
    ('1', 'شخصی'),
    ('2', 'عمومی'),
    ('3', 'اختصاصی'),
)

CLASSIFICATION_CHOICES = (
    ('1', 'عادی'),
    ('2', 'مهم'),
    ('3', 'بسیار مهم'),
)


class Classification(models.Model):
    name = models.CharField(_('نام'), max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = _('طبقه بندی')
        verbose_name_plural = _('طبقه بندی ها')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Inform(models.Model):
    inf_type = models.CharField(_('نوع'), max_length=2, choices=TYPE_CHOICES, default='2')
    roles = models.ManyToManyField(to=Role, blank=True,
                                   help_text='اگر نوع اطلاعیه اختصاصی است  ، نقش های مورد نظر را انتخاب کنید',
                                   verbose_name=_('نقش های مخاطب اطلاعیه'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر مخاطب'),
                             help_text=_('اگر نوع اطلاعیه شخصی باشد نیاز است کاربر مخاطب مشخص شود'), null=True,
                             blank=True)
    topic = models.CharField(_('موضوع'), max_length=200, null=False, blank=False)
    text = models.TextField(_('متن اطلاعیه'), null=False, blank=False)
    inf_classification = models.ForeignKey(to=Classification, on_delete=models.SET_NULL, null=True, blank=False,
                                           verbose_name=_('طبقه بندی'))
    send_notif = models.BooleanField(default=True, verbose_name=_('ارسال نوتیفیکیشن'))
    created_at = models.DateTimeField(_('تاریخ اعلان'), auto_now_add=True)

    class Meta:
        verbose_name = _('اطلاعیه')
        verbose_name_plural = _('اطلاعیه ها ')
        ordering = ('created_at',)

    def __str__(self):
        return self.topic
