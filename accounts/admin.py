from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from sms.models import SendSMS
from . import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _

from jalali_date import datetime2jalali, date2jalali
from django.contrib.sites.shortcuts import get_current_site


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'role', 'is_active', 'is_admin', 'is_staff', 'is_superuser',
                    'get_created_jalali']
    list_editable = ['role', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
    search_fields = ['phone_number', 'first_name']

    actions = ['select_users_for_sms']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ عضویت'

    def select_users_for_sms(self, request, queryset):
        current_domain = get_current_site(request).domain
        if 'apply' in request.POST:
            sms_obj = SendSMS.objects.create()
            sms_obj.recipients.add(*queryset)
            sms_obj.save()
            return HttpResponseRedirect(request.get_full_path())
        context = {
            'users': queryset,
            'domain': current_domain
        }
        return render(request, 'admin/select_users.html', context)

    select_users_for_sms.short_description = _('انتخاب کاربران جهت ارسال پیامک')


@admin.register(models.ProfileCompletionPoints)
class ProfileCompletionPointsAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']


admin.site.unregister(Group)
