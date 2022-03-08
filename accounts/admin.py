from django.contrib import admin
from .adminfilter import UserRoleFilter, UserActiveFilter
from django.utils.html import format_html
from . import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from rangefilter.filters import DateRangeFilter
from jalali_date import datetime2jalali
from ehyasalamat.permission_check import role_permission_checker
from django.contrib.admin.models import LogEntry


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/accounts/role/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/accounts/role/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')

    list_display = ['change_button', 'name', 'delete_button']
    filter_horizontal = ['permissions']
    search_fields = ['name']
    readonly_fields = ['get_permissions_count']

    def get_permissions_count(self, obj):
        return obj.permissions.all().count()

    get_permissions_count.short_description = _('تعداد دسترسی ها')

    def has_add_permission(self, request):
        related_per = 'accounts.add_role'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.change_role'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.view_role'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'accounts.delete_role'
        return role_permission_checker(related_per, request.user)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/accounts/user/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/accounts/user/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'phone_number', 'is_active', 'roles_name',
                    'get_created_jalali', 'delete_button']
    list_filter = [UserRoleFilter, ('date_joined', DateRangeFilter), UserActiveFilter]
    search_fields = ['phone_number', 'first_name', 'role']
    filter_horizontal = ['role', 'user_referrals']
    # autocomplete_fields = ['role']
    # actions = ['select_users_for_sms']
    readonly_fields = ['get_referral_count', 'get_role_count', 'id', 'get_created_jalali']

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "role":
    #         kwargs["queryset"] = self.model.objects.all()
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = [
        ('اطلاعات حساب کاربری', {
            'fields': (
                'id', 'phone_number', 'email', 'password')}),
        ('مشخصات فردی', {
            'fields': (
                'first_name', 'last_name', 'province', 'city', 'birthday', 'gender', 'degree',
                'field_of_study',
                'job')}),
        ('بخش معرفی', {
            'fields': ('referral', 'user_referrals', 'get_referral_count')
        }),
        ('بخش امتیاز', {
            'fields': ('points', 'profile_completion_point')
        }),
        ('بخش سطح کاربری', {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'role', 'get_role_count')
        }),
        ('اطلاعات بیشتر', {
            'fields': ('ip', 'verify_code', 'get_created_jalali')
        }),

    ]

    def roles_name(self, obj):
        roles_list = []
        roles = obj.role.all()
        for role in roles:
            roles_list.append(role.name)
        output = ' , '.join(roles_list)
        return output

    roles_name.short_description = _('نقش های کاربر')

    def get_referral_count(self, obj):
        return obj.user_referrals.all().count()

    def get_role_count(self, obj):
        return obj.role.all().count()

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ عضویت'

    def has_view_permission(self, request, obj=None):
        if request.user.is_staff:
            return True

    get_referral_count.short_description = _('تعداد معرفی')
    get_role_count.short_description = _('تعداد نقش ها')


@admin.register(models.AppUpdate)
class AppUpdateAdmin(admin.ModelAdmin):
    list_display = ['id', 'link', 'value']
    list_editable = ['value', 'link']

    def has_add_permission(self, request):
        related_per = 'accounts.add_appupdate'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.change_appupdate'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.view_appupdate'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'accounts.delete_appupdate'
        return role_permission_checker(related_per, request.user)


@admin.register(models.PointGainHistory)
class PointGainHistoryAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/accounts/pointgainhistory/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/accounts/pointgainhistory/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'user', 'action', 'point', 'get_created_jalali', 'delete_button']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']
    readonly_fields = ['get_created_jalali']

    def has_add_permission(self, request):
        related_per = 'accounts.add_pointgainhistory'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.change_pointgainhistory'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.view_pointgainhistory'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'accounts.delete_pointgainhistory'
        return role_permission_checker(related_per, request.user)

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_created).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'


@admin.register(models.AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/accounts/appsettings/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/accounts/appsettings/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'ticket_answer_limit', 'ticket_cost', 'comment_point', 'support_answer_limit',
                    'profile_completion_point', 'activity_point', 'referral_point', 'delete_button']

    def has_add_permission(self, request):
        related_per = 'accounts.add_appsettings'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.change_appsettings'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.view_appsettings'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'accounts.delete_appsettings'
        return role_permission_checker(related_per, request.user)


admin.site.register(LogEntry)
admin.site.unregister(Group)
admin.site.site_header = 'پنل مدیریت احیا سلامت'








