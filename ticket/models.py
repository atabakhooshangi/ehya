from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('1', 'دیده نشده'),
    ('2', 'پاسخ داده شده'),
    ('3', 'بسته شده')
)


def upload_location(instance, filename):
    extension = filename.split('.')[-1]
    tikcet_id = Ticket.objects.last().id + 1
    return f'uploads/tickets/ticket{tikcet_id}.{extension}'


class Ticket(models.Model):
    user = models.ForeignKey(to=User, verbose_name=_('کاربر'), on_delete=models.CASCADE, null=False, blank=False)
    topic = models.CharField(_('عنوان'), max_length=255, null=False, blank=True)
    section = models.CharField(_('بخش'), max_length=50, null=False, blank=True)
    request_text = models.TextField(_('متن درخواست'), null=False, blank=True)
    file = models.FileField(upload_to=upload_location, verbose_name=_('فایل الصاقی'), null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=_('وضعیت'), max_length=1, default=1)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت ها')
        ordering = ('created_at',)


class Answer(models.Model):
    user = models.ForeignKey(to=User, verbose_name=_('کاربر'), on_delete=models.CASCADE, null=False, blank=False)
    ticket = models.ForeignKey(to=Ticket, verbose_name=_('تیکت مربوطه'), on_delete=models.CASCADE, null=False,
                               blank=False)
    text = models.TextField(_('متن پاسخ'), null=True, blank=True)
    seen_user = models.BooleanField(_('دیده شده توسط کاربر'), default=False)
    seen_admin = models.BooleanField(_('دیده شده توسط ادمین'), default=False)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پاسخ')
        verbose_name_plural = _('پاسخ ها')
        ordering = ('created_at',)
