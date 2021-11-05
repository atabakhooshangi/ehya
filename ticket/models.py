from django.db import models
from django.utils.translation import ugettext as _

STATUS_CHOICES = (
    ('1', 'جدید'),
    ('2', 'در حال بررسی'),
    ('3', 'پاسخ داده شده'),
    ('4', 'بسته شده')
)


def upload_location(instance, filename):
    extension = filename.split('.')[-1]
    tikcet_id = Ticket.objects.last().id + 1
    return f'uploads/tickets/ticket{tikcet_id}.{extension}'


def answer_upload_location(instance, filename):
    extension = filename.split('.')[-1]
    tikcet_id = instance.ticket.id
    answer_id = Ticket.objects.last().id + 1
    return f'uploads/tickets/ticket{tikcet_id}_answer{answer_id}.{extension}'


class Section(models.Model):
    name = models.CharField(_('نام بخش'), max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = _('بخش سلامت')
        verbose_name_plural = _('بخش های سلامت')
        ordering = ('name',)


class Ticket(models.Model):
    user = models.ForeignKey(to='accounts.User', verbose_name=_('کاربر'), on_delete=models.CASCADE, null=False,
                             blank=False)
    topic = models.CharField(_('عنوان'), max_length=255, null=False, blank=True)
    section = models.ForeignKey('Section', on_delete=models.DO_NOTHING, verbose_name=_('بخش مربوطه'), null=False,
                                blank=False)
    request_text = models.TextField(_('متن درخواست'), null=False, blank=True)
    file = models.FileField(upload_to=upload_location, verbose_name=_('فایل ضمیمه'), null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=_('وضعیت'), max_length=1, default=1)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت ها')
        ordering = ('created_at',)


class Answer(models.Model):
    user = models.ForeignKey(to='accounts.User', verbose_name=_('کاربر'), on_delete=models.CASCADE, null=False,
                             blank=False)
    ticket = models.ForeignKey(to=Ticket, verbose_name=_('تیکت مربوطه'), on_delete=models.CASCADE, null=False,
                               blank=False)
    text = models.TextField(_('متن پاسخ'), null=True, blank=True)
    file = models.FileField(upload_to=answer_upload_location, verbose_name=_('فایل ضمیمه'), null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پاسخ')
        verbose_name_plural = _('پاسخ ها')
        ordering = ('created_at',)


class TicketPointCost(models.Model):
    value = models.PositiveIntegerField(default=0, verbose_name=_('مقدار'), null=False, blank=False,
                                        help_text=_('مقدار هزینه امتیاز جهت طرح پرسش توسط کاربر'))

    class Meta:
        verbose_name = _('هزینه پرسش')
        verbose_name_plural = _('هزینه پرسش')
