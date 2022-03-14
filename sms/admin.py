from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from tinymce.widgets import TinyMCE

from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from .models import SendSMS
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from .utils import send_sms


@admin.register(SendSMS)
class SendSmsAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/sms/sendsms/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/sms/sendsms/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    # change_list_template = 'my_change_list/change_list.html'
    list_display = ['change_button', 'topic', 'short_description', 'get_created_jalali', 'delete_button']
    # autocomplete_fields = ['recipients']
    list_filter = [('created_at', DateRangeFilter)]
    search_fields = ['topic']
    # raw_id_fields = ['recipients']
    readonly_fields = ['get_users_count', 'get_role_count']
    filter_horizontal = ['recipients', 'recipients_roles']
    fieldsets = [
        ('موضوع و متن', {
            'fields': (
                'topic', 'text')}),
        ('گیرندگان', {
            'fields': (
                'recipients', 'get_users_count', 'recipients_roles', 'get_role_count')}),
    ]

    # Tiny MCE

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def short_description(self, obj):
        return truncatechars(obj.text, 55)

    short_description.short_description = _('خلاصه متن پیامک')

    def get_users_count(self, obj):
        return obj.recipients.all().count()

    get_users_count.short_description = _('تعداد کاربران انتخاب شده')

    def get_role_count(self, obj):
        return obj.recipients_roles.all().count()

    get_role_count.short_description = _('تعداد نقش های انتخاب شده')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.recipients.clear()
        recipients = form.cleaned_data['recipients']
        first_list = list(recipients.values_list('phone_number', flat=True))
        obj.recipients_roles.clear()
        recipients_roles = form.cleaned_data['recipients_roles']
        users = User.objects.filter(role__in=recipients_roles)
        second_list = list(users.values_list('phone_number', flat=True))
        output = first_list + list(set(second_list) - set(first_list))
        send_sms(message=obj.text, recipients=output)


    def has_add_permission(self, request):
        related_per = 'sms.add_sendsms'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'sms.change_sendsms'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'sms.view_sendsms'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'sms.delete_sendsms'
        return role_permission_checker(related_per, request.user)

