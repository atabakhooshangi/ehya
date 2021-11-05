from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali


@admin.register(models.Inform)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipients', 'classification', 'topic', 'user', 'get_created_jalali', ]

    list_editable = ['classification', 'recipients']
    list_filter = ['recipients', 'classification', 'created_at']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'
