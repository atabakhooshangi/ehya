from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from accounts.models import User , Role

TYPE_CHOICES = (
    ('1', 'شخصی'),
    ('2', 'عمومی'),
    ('3', 'اختصاصی'),
)


def upload_location(instance, filename):
    extension = filename.split('.')[-1]
    return f'uploads/push/push{instance.title}.{extension}'


class PushNotificationSections(models.Model):
    home = models.BooleanField(default=True, verbose_name=_('خانه'))
    inform = models.BooleanField(default=True, verbose_name=_('اعلانات'))
    support = models.BooleanField(default=True, verbose_name=_('پشتیبانی'))
    ticket = models.BooleanField(default=True, verbose_name=_('پرس و پاسخ'))

    class Meta:
        verbose_name = _('بخش های پوش نتیفیکیشن')
        verbose_name_plural = _('بخش های پوش نتیفیکیشن')

    def __str__(self):
        return str(self.id)


class SendPush(models.Model):
    title = models.CharField(_('عنوان'), max_length=120, null=False, blank=False)
    body = models.TextField(_('متن'))
    image = models.ImageField(_('تصویر'), upload_to=upload_location)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر مخاطب'),
                             help_text=_('اگر نوع اطلاعیه شخصی باشد نیاز است کاربر مخاطب مشخص شود'), null=True,
                             blank=True)
    roles = models.ManyToManyField(to=Role, blank=True, verbose_name=_('نقش های گیرندگان'))
    inf_type = models.CharField(_('نوع'), max_length=2, choices=TYPE_CHOICES, default='2')
    date_created = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('ارسال پوش نوتیفیکیشن')
        verbose_name_plural = _('ارسال پوش نوتیفیکیشن')

    def __str__(self):
        return self.title


@receiver(pre_save, sender=SendPush)
def delete_old_file(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
        except sender.DoesNotExist:
            return

        else:
            file = instance.image
            if not old_image == file:
                old_image.delete(save=False)


@receiver(pre_delete, sender=SendPush)
def delete_instance_file(sender, instance, **kwargs):
    instance.image.delete(save=False)
