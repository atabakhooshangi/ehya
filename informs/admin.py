from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from ehyasalamat.permission_check import role_permission_checker
from . import models
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from push_notification.main import PushThread
from django.db.models import QuerySet, Count
from accounts.models import User
from django.utils.translation import ugettext as _


class InformsClassificationSerializer(admin.SimpleListFilter):
    title = _('طبقه بندی')
    parameter_name = 'inf_classification'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(j, k)) for i, j, k in
             qs.values_list('inf_classification__id', 'inf_classification__name').annotate(
                 user_count=Count('inf_classification')).distinct().order_by(
                 'inf_classification__name')]
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
            return queryset.filter(inf_classification=self.value())
        if self.value() == 'all':
            return queryset.all()


class InformsInfTypeSerializer(admin.SimpleListFilter):
    title = _('نوع اطلاعیه')
    parameter_name = 'inf_type'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        a = [(i, "{}  ({})".format(models.TYPE_CHOICES[int(j) - 1][1], k)) for i, j, k in
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


@admin.register(models.Inform)
class InformAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/informs/inform/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/informs/inform/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'inf_type', 'inf_classification', 'topic', 'user', 'get_created_jalali',
                    'delete_button']
    search_fields = ['topic', 'user__phone_number']
    list_filter = [InformsInfTypeSerializer, InformsClassificationSerializer, ('created_at', DateRangeFilter)]
    filter_horizontal = ['roles']
    raw_id_fields = ['user', 'inf_classification']
    autocomplete_fields = ['user', 'inf_classification']
    readonly_fields = ['get_roles_count', 'get_created_jalali']

    fieldsets = [
        ('وارد کردن عنوان و متن اطلاعیه', {
            'fields': (
                'topic', 'text',)}),
        ('مخاطبین اطلاعیه', {
            'fields': (
                'inf_type', 'user', 'roles', 'get_roles_count', 'inf_classification')}),
        ('ارسال پوش', {
            'fields': ('send_notif',)
        }),
        ('تاریخ ایجاد', {
            'fields': ('get_created_jalali',)
        })
    ]

    def get_roles_count(self, obj):
        return obj.roles.all().count()

    get_roles_count.short_description = _('تعداد نقش های انتخاب شده')

    # TinyMCE

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.send_notif:
            if obj.inf_type == '1':
                user = User.objects.filter(id=obj.user.id)
                PushThread(section='inform', title=obj.topic, body=obj.text,
                           push_type='personal', user=user).start()
            elif obj.inf_type == '2':
                PushThread(section='inform', title=obj.topic, body=obj.text,
                           push_type='all').start()
            elif obj.inf_type == '3':
                obj.roles.clear()
                roles = form.cleaned_data['roles']
                users = User.objects.filter(role__in=roles)
                PushThread(section='inform', title=obj.topic, body=obj.text,
                           push_type='group', user=users).start()

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def has_add_permission(self, request):
        related_per = 'informs.add_inform'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'informs.change_inform'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'informs.view_inform'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'informs.delete_inform'
        return role_permission_checker(related_per, request.user)


@admin.register(models.Classification)
class ClassificationAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/informs/classification/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/informs/classification/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')

    list_display = ['change_button', 'name', 'delete_button']
    search_fields = ['name']

    def has_add_permission(self, request):
        related_per = 'informs.add_classification'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'informs.change_classification'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'informs.view_classification'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'informs.delete_classification'
        return role_permission_checker(related_per, request.user)
