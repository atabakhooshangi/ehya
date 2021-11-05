from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
# from jet.filters import RelatedFieldAjaxListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 1


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'topic', 'status', 'file_link', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['status']
    list_filter = ['user', 'status', 'created_at']
    search_fields = ['topic', 'user__phone_number']
    raw_id_fields = ['user']

    def file_link(self, obj):
        if obj.file:
            return format_html(f"<a href='{obj.file.url}' target='_blank'>مشاهده فایل</a>")
            # return format_html(f"<audio controls> <source src='{obj.file.url}'/>مشاهده فایل</audio>")
        return "فایلی آپلود نشده است"

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'
    inlines = [AnswerInLine]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'get_created_jalali']
    list_filter = [('created_at', DateRangeFilter)]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'


@admin.register(models.TicketPointCost)
class TicketPointCostAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']


@admin.register(models.Section)
class TicketPointCostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
