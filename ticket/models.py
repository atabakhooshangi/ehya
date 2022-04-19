from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

USER_STATUS_CHOICES = (
    ('1', 'در حال بررسی'),
    ('2', 'پاسخ داده شده'),
    ('3', 'بسته شده'),
)

EXPERT_STATUS_CHOICES = (
    ('1', 'جدید'),
    ('2', 'ارجاء به کارشناس ارشد'),
    ('3', 'پاسخ داده شده'),
    ('4', 'بسته شده'),
    ('5', 'پاسخ کاربر'),

)

ANSWER_CHOICES = (
    ('1', 'دیده شده'),
    ('2', 'دیده نشده'),
)


def upload_location(instance, filename):
    extension = filename.split('.')[-1]
    if len(Ticket.objects.all()) > 0:
        ticket_id = Ticket.objects.last().id + 1
    else:
        ticket_id = 1
    return f'uploads/tickets/ticket{ticket_id}.{extension}'


def answer_upload_location(instance, filename):
    extension = filename.split('.')[-1]
    ticket_id = instance.ticket.id
    answer_id = Ticket.objects.last().id + 1
    return f'uploads/tickets/ticket{ticket_id}_answer{answer_id}.{extension}'


def channel_icon_upload_location(instance, filename):
    extension = filename.split('.')[-1]
    return f'uploads/tickets/ticket{filename}.{extension}'


# class TicketAnswerLimit(models.Model):
#     value = models.PositiveIntegerField(_('مقدار'), default=3, help_text=_(
#         'مقدار وارد شده تعیین میکند که کاربر حداکثر تا چند پاسخ در بدنه پرسش خود میتواند مطرح کند.'))
#
#     class Meta:
#         verbose_name = _('محدودیت تعداد پاسخ')
#         verbose_name_plural = _('محدودیت تعداد پاسخ')


class Section(models.Model):
    name = models.CharField(_('نام بخش'), max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = _('بخش سلامت')
        verbose_name_plural = _('بخش های سلامت')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    user = models.ForeignKey(to='accounts.User', verbose_name=_('کاربر'), on_delete=models.CASCADE, null=False,
                             blank=False)
    topic = models.CharField(_('عنوان'), max_length=255, null=False, blank=True)
    section = models.ForeignKey('Section', on_delete=models.DO_NOTHING, verbose_name=_('بخش مربوطه'), null=False,
                                blank=False)
    request_text = models.TextField(_('متن درخواست'), null=False, blank=True)
    file = models.FileField(upload_to=upload_location, verbose_name=_('فایل ضمیمه'), null=True, blank=True)
    status_for_user = models.CharField(choices=USER_STATUS_CHOICES, verbose_name=_('وضعیت برای کاربر'), max_length=1,
                                       default=1)
    status_for_expert = models.CharField(choices=EXPERT_STATUS_CHOICES, verbose_name=_('وضعیت برای کارشناس'),
                                         max_length=1,
                                         default=1)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت ها')
        ordering = ('created_at',)

    def __str__(self):
        return f' تیکت {self.user} '


class Answer(models.Model):
    user = models.ForeignKey(to='accounts.User', verbose_name=_('کاربر'), on_delete=models.CASCADE, null=True,
                             blank=True)
    ticket = models.ForeignKey(to=Ticket, verbose_name=_('تیکت مربوطه'), on_delete=models.CASCADE, null=False,
                               blank=False)
    text = models.TextField(_('متن پاسخ'), null=True, blank=True)
    file = models.FileField(upload_to=answer_upload_location, verbose_name=_('فایل ضمیمه'), null=True, blank=True)
    status = models.CharField(choices=ANSWER_CHOICES, verbose_name=_('وضعیت'), max_length=1, default=2)
    seen_at = models.DateTimeField(verbose_name=_('تاریخ دیده شدن'), null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پاسخ')
        verbose_name_plural = _('پاسخ ها')
        ordering = ('created_at',)

    def __str__(self):
        return str(self.id)


# class TicketPointCost(models.Model):
#     value = models.PositiveIntegerField(default=0, verbose_name=_('مقدار'), null=False, blank=False,
#                                         help_text=_('مقدار هزینه امتیاز جهت طرح پرسش توسط کاربر'))
#
#     class Meta:
#         verbose_name = _('هزینه پرسش')
#         verbose_name_plural = _('هزینه پرسش')

class Channels(models.Model):
    title = models.CharField(_('عنوان'), max_length=50, null=False, blank=False)
    icon = models.ImageField(_('آیکون'), upload_to=channel_icon_upload_location, null=True, blank=True)
    description = models.TextField(_('توضیحات'), null=False, blank=False)
    link = models.CharField(_('لینک'), max_length=255, null=False, blank=False)
    back_ground_colour_1 = models.CharField(_('رنگ بک گراند 1'), max_length=50, null=True, blank=True)
    back_ground_colour_2 = models.CharField(_('رنگ بک گراند 2'), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _('گروه و کانال')
        verbose_name_plural = _('گروه ها و کانال ها')
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def icon_preview(self):
        if self.icon:
            return mark_safe('<img src="{}" width="200" height="120" />'.format(self.icon.url))
        return "موردی یافت نشد"
