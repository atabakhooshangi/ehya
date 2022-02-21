from django.contrib import admin

from ehyasalamat.permission_check import role_permission_checker
from . import models
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from push_notification.main import PushThread
from django.db.models import QuerySet
from accounts.models import User


@admin.register(models.Inform)
class InformAdmin(admin.ModelAdmin):
    list_display = ['id', 'inf_type', 'classification', 'topic', 'user', 'get_created_jalali', ]
    search_fields = ['topic', 'user__phone_number']
    list_editable = ['classification', 'inf_type']
    list_filter = ['inf_type', 'classification', ('created_at', DateRangeFilter)]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.inf_type == '1':
            user = User.objects.filter(id=obj.user.id)
            PushThread(section='inform', title=obj.topic, body=obj.text,
                       push_type='personal', user=user).start()
        elif obj.inf_type == '2':
            PushThread(section='inform', title=obj.topic, body=obj.text,
                       push_type='all').start()
        elif obj.inf_type == '3':
            obj.roles.clear()
            roles = form.cleaned_data['roles']
            users = User.objects.filter(role__in=roles)
            PushThread(section='inform', title=obj.topic, body=obj.text,
                       push_type='group', user=users).start()

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def has_add_permission(self, request):
        related_per = 'informs.add_inform'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'informs.change_inform'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'informs.view_inform'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'informs.delete_inform'
        return role_permission_checker(related_per, request.user)
