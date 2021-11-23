from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali


@admin.register(models.Inform)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'inf_type', 'classification', 'topic', 'user', 'get_created_jalali', ]

    list_editable = ['classification', 'inf_type']
    list_filter = ['inf_type', 'classification', 'created_at']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'
