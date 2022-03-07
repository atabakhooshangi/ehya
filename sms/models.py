from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from accounts.models import Role, User


# SMS_TYPE_CHOICES = (
#     ('1', 'عمومی'),
#     ('2', 'شخصی'),
# )


class SendSMS(models.Model):
    recipients = models.ManyToManyField(to=User, verbose_name='گیرندگان', blank=True)
    recipients_roles = models.ManyToManyField(to=Role, verbose_name='گیرندگان', blank=True)
    topic = models.CharField(_('موضوع'), max_length=225, null=True, blank=False)
    text = models.TextField(_('متن پیامک'), null=True, blank=False)
    # sms_type = models.CharField(_('نوع پیام'), max_length=10, choices=SMS_TYPE_CHOICES, default='1',
    # help_text='اگر در متن پیامک متغیر نسبت به کاربر وجود دارد گزینه شخصی اتخاب شود و در غیر اینصورت گزینه عمومی')
    created_at = models.DateTimeField(_('تاریخ ارسال'), auto_now_add=True)

    class Meta:
        verbose_name = _('پیامک')
        verbose_name_plural = _('پیامک ها')
        ordering = ('created_at',)

    def __str__(self):
        if not self.topic:
            return str(self.id)
        return str(self.topic)
