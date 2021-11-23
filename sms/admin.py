from django.contrib import admin
from .models import SendSMS
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


@admin.register(SendSMS)
class SendSmsAdmin(admin.ModelAdmin):
    # change_list_template = 'my_change_list/change_list.html'
    list_display = ['topic', 'get_created_jalali', 'recep']
    autocomplete_fields = ['recipients']
    list_filter = [('created_at', DateRangeFilter)]
    search_fields = ['topic']
    raw_id_fields = ['recipients']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def recep(self, obj):
        return obj.recipients.count()

    def has_add_permission(self, request):
        if request.user.is_staff:
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_staff:
            return True

    recep.short_description = 'تعداد گیرندگان'
