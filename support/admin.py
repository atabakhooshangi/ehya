from django.contrib import admin
from .models import SupportTicket, SupportAnswer, SupportSection, SupportTicketAnswerLimit
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html


class SupportAnswerInLine(admin.TabularInline):
    model = SupportAnswer
    extra = 0
    autocomplete_fields = ['user']
    readonly_fields = ['user']
    fields = ['text', 'user']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'section', 'topic', 'status', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['section', 'status']
    list_filter = ['user', 'status', 'created_at']
    search_fields = ['topic', 'user__phone_number']
    raw_id_fields = ['user']
    inlines = [SupportAnswerInLine]

    fieldsets = [
        ('موضوع', {
            'fields': ('topic',)
        }),
        ('مشخصات کلی', {
            'fields': ('user', ('request_text', 'status'))
        })]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'


@admin.register(SupportSection)
class SupportSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    list_editable = ['name', 'active']


@admin.register(SupportTicketAnswerLimit)
class SupportTicketAnswerLimitAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
