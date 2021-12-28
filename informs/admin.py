from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


@admin.register(models.Inform)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'inf_type', 'classification', 'topic', 'user', 'get_created_jalali', ]
    search_fields = ['topic','user__phone_number']
    list_editable = ['classification', 'inf_type']
    list_filter = ['inf_type', 'classification', ('created_at', DateRangeFilter)]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def has_add_permission(self, request):
        related_per = 'informs.add_inform'
        if related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'informs.change_inform'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'informs.view_inform'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'informs.delete_inform'
        if related_per in request.user.get_user_permissions():
            return True
