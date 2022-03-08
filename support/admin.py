from django.contrib import admin
from django.utils.translation import ugettext as _
from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from push_notification.main import PushThread
from .models import SupportTicket, SupportAnswer, SupportSection  # SupportTicketAnswerLimit
from jalali_date import datetime2jalali
from rangefilter.filters import DateRangeFilter
from django.utils.html import format_html
from .admin_filter import SupportTicketSectionFilter, SupportTicketStatusFilter


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
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/support/supportticket/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/support/supportticket/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'user', 'section', 'topic', 'status_for_user', 'status_for_support',
                    'get_created_jalali', 'delete_button']
    autocomplete_fields = ['user']
    list_filter = [SupportTicketStatusFilter, SupportTicketSectionFilter, ('created_at', DateRangeFilter)]
    search_fields = ['topic', 'user__phone_number', 'user__first_name', 'user__last_name', 'section']
    raw_id_fields = ['user']
    inlines = [SupportAnswerInLine]
    readonly_fields = ['get_created_jalali','id']

    fieldsets = [
        ('موضوع و شناسه', {
            'fields': ('topic','id')
        }),
        ('مشخصات کلی', {
            'fields': ('user', 'section', 'request_text', 'status_for_user', 'status_for_support','get_created_jalali')
        })]

    def save_formset(self, request, form, formset, change):
        user = form.cleaned_data['user']
        instances = formset.save(commit=False)
        user = User.objects.filter(id=user.id)
        for instance in instances:
            instance.save()
            if not instance.user:
                status_for_supp = form.cleaned_data['status_for_support']
                status_for_user = form.cleaned_data['status_for_user']
                if status_for_supp != '3' and status_for_user != '3':
                    instance.user = request.user
                    instance.save()
                    instance.ticket.status_for_user = '2'
                    instance.ticket.status_for_support = '2'
                    instance.ticket.save()
                admin_answers = instance.ticket.supportanswer_set.filter(user=instance.ticket.user)
                for answ in admin_answers:
                    answ.status = '1'
                    answ.save()
            PushThread(section='support', title=instance.ticket.topic, body=instance.text,
                       push_type='personal', user=user).start()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):

        if obj.status_for_user == '3' and obj.status_for_support != '3':
            obj.status_for_support = '3'
        if obj.status_for_support == '3' and obj.status_for_user != '3':
            obj.status_for_user = '3'
        super().save_model(request, obj, form, change)

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
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/support/supportsection/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/support/supportsection/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    filter_horizontal = ['associated_roles']
    list_display = ['change_button', 'name', 'active', 'delete_button']

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

