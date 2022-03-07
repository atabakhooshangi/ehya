from django.conf import settings
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali
from tinymce.widgets import TinyMCE

from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from .main import PushThread
from .models import PushNotificationSections, SendPush, upload_location, TYPE_CHOICES


class PushInfTypeSerializer(admin.SimpleListFilter):
    title = _('نوع پوش')
    parameter_name = 'inf_type'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(TYPE_CHOICES[int(j) - 1][1], k)) for i, j, k in
             qs.values_list('inf_type', 'inf_type').annotate(
                 user_count=Count('inf_type')).distinct().order_by(
                 'inf_type')]
        t = ('all', f'همه ({qs.count()})')
        a.insert(0, t)
        return a

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() and self.value() != 'all':  # Use the lookup id we sent above; to filter
            return queryset.filter(inf_type=self.value())
        if self.value() == 'all':
            return queryset.all()


@admin.register(PushNotificationSections)
class PushNotifAdmin(admin.ModelAdmin):
    list_display = ['id', 'home', 'support', 'ticket', 'inform']
    list_editable = ['home', 'support', 'ticket', 'inform']

    def has_add_permission(self, request):
        related_per = 'push_notification.add_pushnotificationsections'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'push_notification.change_pushnotificationsections'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.view_pushnotificationsections'
        return role_permission_checker(related_per, request.user)


@admin.register(SendPush)
class SendPushAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/push_notification/sendpush/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/push_notification/sendpush/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = [_('change_button'), 'title', 'image', 'inf_type', 'date_created', 'delete_button']
    filter_horizontal = ['roles']
    search_fields = ['roles__name', 'user__phone_number', 'title', 'inf_type']
    autocomplete_fields = ['user']
    list_filter = [PushInfTypeSerializer]
    readonly_fields = ['get_created_jalali', 'get_roles_count', 'thumbnail_preview']
    fieldsets = [
        ('وارد کردن عنوان و متن پوش', {
            'fields': (
                'title', 'body', 'image', 'thumbnail_preview')}),
        ('مخاطبین پوش', {
            'fields': (
                'inf_type', 'user', 'roles', 'get_roles_count')}),
        ('تاریخ ایجاد', {
            'fields': ('get_created_jalali',)
        })
    ]

    def thumbnail_preview(self, obj):
        return mark_safe('<img src="{}" width="280" height="200" />'.format(obj.image.url))

    thumbnail_preview.short_description = 'پیش نمایش'

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def get_roles_count(self, obj):
        return obj.roles.all().count()

    get_roles_count.short_description = _('تعداد نقش های انتخاب شده')

    def has_add_permission(self, request):
        related_per = 'push_notification.add_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'push_notification.change_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.view_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'push_notification.delete_sendpush'
        return role_permission_checker(related_per, request.user)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        photo_url = upload_location(obj, str(obj.image))
        url = 'http://' + get_current_site(request).domain + settings.MEDIA_URL + photo_url
        if obj.inf_type == '1':
            user = User.objects.filter(id=obj.user.id)
            PushThread(section='push', title=obj.title, body=obj.body,
                       push_type='personal', user=user, image=str(url)).start()
        elif obj.inf_type == '2':
            PushThread(section='push', title=obj.title, body=obj.body,
                       push_type='all', image=str(url)).start()
        elif obj.inf_type == '3':
            obj.roles.clear()
            roles = form.cleaned_data['roles']
            users = User.objects.filter(role__in=roles)
            PushThread(section='push', title=obj.title, body=obj.body,
                       push_type='group', user=users, image=str(url)).start()
        # if obj.send_to_all:
        #     PushThread(section='push', title=obj.title, body=obj.body, image=str(url),
        #                push_type='all').start()
        # else:
        #     print('group')
        #     obj.receptors.clear()
        #     users = form.cleaned_data['receptors']
        #     PushThread(section='push', title=obj.title, body=obj.body, image=str(url),
        #                push_type='group', user=users).start()

    # Tiny MCE

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'body':
    #         return db_field.formfield(widget=TinyMCE(
    #             attrs={'cols': 80, 'rows': 30},
    #             mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
    #         ))
    #     return super().formfield_for_dbfield(db_field, **kwargs)
