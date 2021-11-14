from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('1', 'جدید'),
    ('2', 'در حال بررسی'),
    ('3', 'پاسخ داده شده'),
    ('4', 'پاسخ کاربر'),
    ('5', 'بسته شده')
)


class SupportTicket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, verbose_name=_('کاربر'), null=False, blank=False)
    topic = models.CharField(_('موضوع'), max_length=255, null=False, blank=False)
    # section = models.ForeignKey('Section', on_delete=models.DO_NOTHING, verbose_name=_('بخش مربوطه'), null=False,
    #                             blank=False)
    request_text = models.TextField(_('متن درخواست'), null=False, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=_('وضعیت'), max_length=1, default=1)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تیکت پشتیانی')
        verbose_name_plural = _('تیکت های پشتیبانی')
        ordering = ('created_at', 'topic')


class SupportAnswer(models.Model):
    admin_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    ticket = models.ForeignKey(to=SupportTicket, on_delete=models.DO_NOTHING, verbose_name=_('تیکت پشتیبانی'),
                               null=False, blank=False)
    text = models.TextField(_('متن پاسخ'))
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پاسخ پشتیبانی')
        verbose_name_plural = _('پاسخ های پشتیبانی')
        ordering = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()
