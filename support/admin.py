from django.contrib import admin

from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from push_notification.main import PushThread
from .models import SupportTicket, SupportAnswer, SupportSection, SupportTicketAnswerLimit
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html


class SupportAnswerInLine(admin.TabularInline):
    model = SupportAnswer
    extra = 0
    autocomplete_fields = ['user']
    # readonly_fields = ['user']
    fields = ['text', 'user', 'status', 'id']

    def has_add_permission(self, request, obj=None):
        related_per = 'support.add_supportanswer'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'support.change_supportanswer'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'support.view_supportanswer'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'support.delete_supportanswer'
        return role_permission_checker(related_per, request.user)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'section', 'topic', 'status_for_user', 'status_for_support', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['section', 'status_for_user', 'status_for_support']
    list_filter = ['section', 'status_for_user', 'status_for_support', ('created_at', DateRangeFilter)]
    search_fields = ['topic', 'user__phone_number']
    raw_id_fields = ['user']
    inlines = [SupportAnswerInLine]

    fieldsets = [
        ('موضوع', {
            'fields': ('topic',)
        }),
        ('مشخصات کلی', {
            'fields': ('user', 'section', ('request_text', 'status_for_user', 'status_for_support'))
        })]

    def save_formset(self, request, form, formset, change):
        user = form.cleaned_data['user']
        instances = formset.save(commit=False)
        user = User.objects.filter(id=user.id)
        for instance in instances:
            instance.user = request.user
            instance.save()
            PushThread(section='support', title=instance.ticket.topic, body=instance.text,
                       push_type='personal', user=user).start()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        user_roles = request.user.role.all()
        section = SupportSection.objects.filter(associated_roles__in=user_roles)
        query = SupportTicket.objects.filter(section__in=section)
        return query

    def has_add_permission(self, request):
        related_per = 'support.add_supportticket'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'support.change_supportticket'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'support.view_supportticket'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'support.delete_supportticket'
        return role_permission_checker(related_per, request.user)


@admin.register(SupportSection)
class SupportSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    list_editable = ['name', 'active']

    def has_add_permission(self, request):
        related_per = 'support.add_supportsection'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'support.change_supportsection'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'support.view_ssupportsection'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'support.delete_supportsection'
        return role_permission_checker(related_per, request.user)


@admin.register(SupportTicketAnswerLimit)
class SupportTicketAnswerLimitAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        related_per = 'support.add_supportticketanswerlimit'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'support.change_supportticketanswerlimit'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'support.view_supportticketanswerlimit'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'support.delete_supportticketanswerlimit'
        return role_permission_checker(related_per, request.user)
