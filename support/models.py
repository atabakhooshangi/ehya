from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from accounts.models import Role

User = get_user_model()

# STATUS_CHOICES = (
#     ('1', 'جدید'),
#     ('2', 'در حال بررسی'),
#     ('3', 'پاسخ داده شده'),
#     ('4', 'پاسخ کاربر'),
#     ('5', 'بسته شده')
# )

USER_STATUS_CHOICES = (
    ('1', 'در حال بررسی'),
    ('2', 'پاسخ داده شده'),
    ('3', 'بسته شده'),
)

SUPPORT_STATUS_CHOICES = (
    ('1', 'جدید'),
    ('2', 'پاسخ داده شده'),
    ('3', 'بسته شده'),
    ('4', 'پاسخ کاربر'),

)

ANSWER_CHOICES = (
    ('1', 'دیده شده'),
    ('2', 'دیده نشده'),
)


class SupportSection(models.Model):
    name = models.CharField(_('نام بخش'), max_length=150, null=False, blank=False)
    associated_roles = models.ManyToManyField(to=Role, blank=True, verbose_name=_('نقش های مربوطه'))
    active = models.BooleanField(_('فعال'), default=True)

    class Meta:
        verbose_name = _('بخش پشتیبانی')
        verbose_name_plural = _('بخش های پشتیبانی')
        ordering = ('name',)

    def __str__(self):
        return self.name


class SupportTicket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'), null=True, blank=True)
    topic = models.CharField(_('موضوع'), max_length=255, null=False, blank=False)
    section = models.ForeignKey(to=SupportSection, on_delete=models.CASCADE, verbose_name=_('بخش مربوطه'),
                                null=False,
                                blank=False)
    request_text = models.TextField(_('متن درخواست'), null=False, blank=True)
    status_for_user = models.CharField(choices=USER_STATUS_CHOICES, verbose_name=_('وضعیت برای کاربر'), max_length=1,
                                       default=1)
    status_for_support = models.CharField(choices=SUPPORT_STATUS_CHOICES, verbose_name=_('وضعیت برای پشتیبان'),
                                          max_length=1,
                                          default=1)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تیکت پشتیانی')
        verbose_name_plural = _('تیکت های پشتیبانی')
        ordering = ('created_at', 'topic')

    def __str__(self):
        return f' تیکت پشتیبانی {self.user} '


class SupportAnswer(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    ticket = models.ForeignKey(to=SupportTicket, on_delete=models.CASCADE, verbose_name=_('تیکت پشتیبانی'),
                               null=False, blank=False)
    text = models.TextField(_('متن پاسخ'))
    status = models.CharField(choices=ANSWER_CHOICES, verbose_name=_('وضعیت'), max_length=1, default=2)
    seen_at = models.DateTimeField(verbose_name=_('تاریخ دیده شدن'), null=True, blank=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پاسخ پشتیبانی')
        verbose_name_plural = _('پاسخ های پشتیبانی')
        ordering = ('created_at',)

    def __str__(self):
        return f"support ticket {self.ticket.id}'s answer with id {str(self.id)}"


# class SupportTicketAnswerLimit(models.Model):
#     value = models.PositiveIntegerField(_('مقدار'), default=3, help_text=_(
#         'مقدار وارد شده تعیین میکند که کاربر حداکثر تا چند پاسخ در بدنه تیکت پشتیبانی خود میتواند مطرح کند.'))
#
#     class Meta:
#         verbose_name = _('محدودیت تعداد پاسخ تیکت پشتیبانی')
#         verbose_name_plural = _('محدودیت تعداد پاسخ تیکت پشتیبانی ')
