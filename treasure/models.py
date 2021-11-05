from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model

User = get_user_model()


class Treasury(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'), null=False, blank=False)
    topic = models.CharField(_('موضوع'), max_length=225, null=False, blank=False)
    link = models.URLField(_('لینک مطلب'),null=False,blank=True)

