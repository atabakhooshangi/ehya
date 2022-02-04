from django.contrib import admin

from accounts.models import User
from . import models
from jalali_date import datetime2jalali, date2jalali
# from jet.filters import RelatedFieldAjaxListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html
from push_notification.main import PushThread


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 0
    autocomplete_fields = ['user']
    readonly_fields = ['user']
    fields = ['text', 'file', 'status', 'user']

    def has_add_permission(self, request, obj=None):
        related_per = 'ticket.add_answer'
        if related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_answer'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_answer'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_answer'
        if related_per in request.user.get_user_permissions():
            return True


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'topic', 'status_for_user', 'status_for_expert', 'file_link', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['status_for_user', 'status_for_expert']
    list_filter = ['status_for_user', 'status_for_expert', ('created_at', DateRangeFilter)]
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

    def has_add_permission(self, request, obj=None):
        related_per = 'ticket.add_ticket'
        if related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_ticket'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_ticket'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_ticket'
        if related_per in request.user.get_user_permissions():
            return True

    inlines = [AnswerInLine]

    def save_formset(self, request, form, formset, change):
        user = form.cleaned_data['user']
        instances = formset.save(commit=False)
        user = User.objects.filter(id=user.id)
        for instance in instances:
            instance.user = request.user
            instance.save()
            PushThread(section='ticket', title=instance.ticket.topic, body=instance.text,
                       push_type='personal', user=user).start()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()


# @admin.register(models.Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ['user', 'ticket', 'get_created_jalali']
#     list_filter = [('created_at', DateRangeFilter)]
#     autocomplete_fields = ['user']
#     search_fields = ['user__phone_number']
#     raw_id_fields = ['user']
#
#     def get_created_jalali(self, obj):
#         return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')
#
#     get_created_jalali.short_description = 'تاریخ ایجاد'
#
#     def has_view_permission(self, request, obj=None):
#         if request.user.role:
#             if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
#                 return True
#
#     def has_change_permission(self, request, obj=None):
#         if request.user.role:
#             if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
#                 return True
#
#     def has_add_permission(self, request):
#         if request.user.role:
#             if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
#                 return True
#
#     def has_delete_permission(self, request, obj=None):
#         if request.user.is_admin:
#             return True


@admin.register(models.TicketPointCost)
class TicketPointCostAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        related_per = 'ticket.add_ticketpointcost'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_ticketpointcost'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_ticketpointcost'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_ticketpointcost'
        if related_per in request.user.get_user_permissions():
            return True


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


@admin.register(models.TicketAnswerLimit)
class TicketAnswerLimitAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        related_per = 'ticket.add_ticketanswerlimit'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_ticketanswerlimit'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_ticketanswerlimit'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_ticketanswerlimit'
        if related_per in request.user.get_user_permissions():
            return True
