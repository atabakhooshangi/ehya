from django.contrib import admin
from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from . import models
from jalali_date import datetime2jalali
# from jet.filters import RelatedFieldAjaxListFilter
from rangefilter.filters import DateRangeFilter
from django.utils.html import format_html
from push_notification.main import PushThread
from django.utils.translation import ugettext as _
from .admin_filter import TicketExpertStatusSerializer, TicketSectionFilter
from django.urls import reverse
from tinymce.widgets import TinyMCE


# class TicketUserStatusSerializer(admin.SimpleListFilter):
#     title = _('وضعیت برای کاربر')
#     parameter_name = 'status_for_user'
#
#     def lookups(self, request, model_admin):
#         # print(USER_STATUS_CHOICES[0][1], USER_STATUS_CHOICES[2])
#         qs = model_admin.get_queryset(request)
#         a = [(i, "{}  ({})".format(USER_STATUS_CHOICES[int(j) - 1][1], k)) for i, j, k in
#              qs.values_list('status_for_user', 'status_for_user').annotate(
#                  user_count=Count('status_for_user')).distinct().order_by(
#                  'status_for_user')]
#         t = ('all', f'همه ({qs.count()})')
#         a.insert(0, t)
#         return a
#
#     def choices(self, changelist):
#         yield {
#             'selected': self.value() is None,
#             'query_string': changelist.get_query_string(remove=[self.parameter_name]),
#         }
#         for lookup, title in self.lookup_choices:
#             yield {
#                 'selected': self.value() == str(lookup),
#                 'query_string': changelist.get_query_string({self.parameter_name: lookup}),
#                 'display': title, }
#
#     def queryset(self, request, queryset):
#         if self.value() and self.value() != 'all':  # Use the lookup id we sent above; to filter
#             return queryset.filter(status_for_user=self.value())
#         if self.value() == 'all':
#             print('all')
#             return queryset.all()


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 0
    autocomplete_fields = ['user']
    readonly_fields = ['user', 'id', 'get_created_jalali']
    fields = ['text', 'file', 'status', 'user', 'get_created_jalali']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def has_add_permission(self, request, obj=None):
        related_per = 'ticket.add_answer'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_answer'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_answer'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_answer'
        return role_permission_checker(related_per, request.user)


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/ticket/ticket/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/ticket/ticket/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'user', 'topic', 'status_for_user', 'status_for_expert', 'file_link',
                    'get_created_jalali', 'delete_button']
    autocomplete_fields = ['user']
    list_filter = [TicketExpertStatusSerializer, TicketSectionFilter, ('created_at', DateRangeFilter)]
    search_fields = ['topic', 'user__phone_number', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']
    readonly_fields = ['get_created_jalali', 'id']
    fieldsets = [
        ('موضوع و شناسه', {
            'fields': ('topic', 'id')
        }),
        ('مشخصات کلی', {
            'fields': ('user', 'section', 'request_text', 'status_for_user', 'status_for_expert', 'get_created_jalali')
        })]

    def file_link(self, obj):
        if obj.file:
            return format_html(f"<a href='{obj.file.url}' target='_blank'>مشاهده فایل</a>")
            # return format_html(f"<audio controls> <source src='{obj.file.url}'/>مشاهده فایل</audio>")
        return "موردی یافت نشد"

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'request_text':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def has_add_permission(self, request, obj=None):
        related_per = 'ticket.add_ticket'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'ticket.change_ticket'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'ticket.view_ticket'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'ticket.delete_ticket'
        return role_permission_checker(related_per, request.user)

    inlines = [AnswerInLine]

    def save_formset(self, request, form, formset, change):
        user = form.cleaned_data['user']
        instances = formset.save(commit=False)
        user = User.objects.filter(id=user.id)
        for instance in instances:
            instance.save()
            if not instance.user:
                status_for_ex = form.cleaned_data['status_for_expert']
                status_for_user = form.cleaned_data['status_for_user']
                if status_for_ex != '4' and status_for_user != '3':
                    instance.user = request.user
                    instance.save()
                    instance.ticket.status_for_user = '2'
                    instance.ticket.status_for_expert = '3'
                    instance.ticket.save()
                admin_answers = instance.ticket.answer_set.filter(user=instance.ticket.user)
                for answ in admin_answers:
                    answ.status = '1'
                    answ.save()

            PushThread(section='ticket', title=instance.ticket.topic, body=instance.text,
                       push_type='personal', user=user).start()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):

        if obj.status_for_user == '3' and obj.status_for_expert != '4':
            obj.status_for_expert = '4'
        if obj.status_for_expert == '4' and obj.status_for_user != '3':
            obj.status_for_user = '3'
        super().save_model(request, obj, form, change)


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


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):

    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/ticket/section/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/ticket/section/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'name', 'delete_button']
    list_editable = ['name']
    search_fields = ['name']


@admin.register(models.Channels)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link']
