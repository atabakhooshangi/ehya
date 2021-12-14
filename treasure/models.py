from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


def file_size(value):  # add this to some file where you can import it from
    limit = 7 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('حجم فایل نمیتواند بیشتر از 5 مگابایت باشد.'))


def upload_location(instance, filename):
    extension = filename.split('.')[-1]
    if len(Treasury.objects.all()) > 0:
        treasure_id = Treasury.objects.last().id + 1
    else:
        treasure_id = 1
    return f'uploads/treasury/Treasury{treasure_id}.{extension}'


class Treasury(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'), null=False, blank=False)
    topic = models.CharField(_('موضوع'), max_length=225, null=False, blank=False)
    link = models.URLField(_('لینک مطلب'), null=False, blank=True)
    file = models.FileField(upload_to=upload_location, verbose_name=_('فایل ارسالی'), null=True, blank=True,
                            validators=[file_size]
                            )
    created_at = models.DateTimeField(verbose_name=_('تاریخ ارسال'), auto_now_add=True)

    class Meta:
        verbose_name = _('گنجینه')
        verbose_name_plural = _('گنجینه ها')
        ordering = ('created_at',)

    def __str__(self):
        return f' گنجینه {self.id} '


class TreasureAnswer(models.Model):
    text = models.TextField(_('متن پیام تشکر'))

    class Meta:
        verbose_name = _('متن پیام تشکر گنجینه')
        verbose_name_plural = _('متن پیام تشکر گنجینه')

    def __str__(self):
        return self.text
