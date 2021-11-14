from django.contrib import admin
from .models import SupportTicket, SupportAnswer
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html


class SupportAnswerInLine(admin.TabularInline):
    model = SupportAnswer
    extra = 0
    autocomplete_fields = ['admin_user']


@admin.register(SupportTicket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'topic', 'status', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['status']
    list_filter = ['user', 'status', 'created_at']
    search_fields = ['topic', 'user__phone_number']
    raw_id_fields = ['user']
    inlines = [SupportAnswerInLine]

    fieldsets = [
        ('Standard info', {
            'fields': ('topic',)
        }),
        ('Address info', {
            'fields': ('user', ('request_text', 'status'))
        })]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'
