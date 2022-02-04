from django.db import models
from django.utils.translation import ugettext as _


class PushNotificationSections(models.Model):
    home = models.BooleanField(default=True, verbose_name=_('خانه'))
    inform = models.BooleanField(default=True, verbose_name=_('اعلانات'))
    support = models.BooleanField(default=True, verbose_name=_('پشتیبانی'))
    ticket = models.BooleanField(default=True, verbose_name=_('پرس و پاسخ'))
    treasure = models.BooleanField(default=True, verbose_name=_('گنجینه'))

    class Meta:
        verbose_name = _('بخش های پوش نتیفیکیشن')
        verbose_name_plural = _('بخش های پوش نتیفیکیشن')

    def __str__(self):
        return str(self.id)
