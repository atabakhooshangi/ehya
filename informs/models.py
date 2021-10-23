from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model

User = get_user_model()

RECIPIENTS_CHOICES = (
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
    ('14', 'عمومی'),
    ('15', 'خصوصی'),
)

CLASSIFICATION_CHOICES = (
    ('1', 'عادی'),
    ('2', 'مهم'),
    ('3', 'بسیار مهم'),
)


class Inform(models.Model):
    recipients = models.CharField(_('مخاطبین'), max_length=2, choices=RECIPIENTS_CHOICES, default='14')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر مخاطب'),
                             help_text=_('اگر نوع اطلاعیه شخصی باشد نیاز است کاربر مخاطب مشخص شود'), null=True,
                             blank=True)
    topic = models.CharField(_('موضوع'), max_length=200, null=False, blank=False)
    text = models.TextField(_('متن اطلاعیه'), null=False, blank=False)
    classification = models.CharField(_('طبقه بندی'), max_length=15, choices=CLASSIFICATION_CHOICES, default=1)
    created_at = models.DateTimeField(_('تاریخ اعلان'), auto_now_add=True)

    class Meta:
        verbose_name = _('اطلاعیه')
        verbose_name_plural = _('اطلاعیه ها')
        ordering = ('created_at',)
