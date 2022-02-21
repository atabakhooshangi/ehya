from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from sms.models import SendSMS
from . import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from rangefilter.filters import DateRangeFilter
from jalali_date import datetime2jalali
from django.contrib.sites.shortcuts import get_current_site
from ehyasalamat.permission_check import role_permission_checker


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    filter_horizontal = ['permissions']

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
    list_display = ['id', 'phone_number', 'is_active', 'is_admin', 'is_staff', 'is_superuser',
                    'get_created_jalali']
    list_editable = ['is_active', 'is_admin', 'is_staff', 'is_superuser']
    list_filter = ['role', ('date_joined', DateRangeFilter), 'is_active', 'is_admin', 'is_staff', 'is_superuser']
    search_fields = ['phone_number', 'first_name']
    filter_horizontal = ['role']
    actions = ['select_users_for_sms']

    fieldsets = [
        ('اطلاعات تماس', {
            'fields': (
                'phone_number', 'email', 'password')}),
        ('مشخصات فردی', {
            'fields': (
                'first_name', 'last_name', 'province', 'city', 'birthday', 'gender', 'degree',
                'field_of_study',
                'job')}),
        ('بخش معرفی', {
            'fields': ('referral', 'user_referrals')
        }),
        ('بخش امتیاز', {
            'fields': ('points', 'profile_completion_point')
        }),
        ('بخش سطح کاربری', {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'role')
        }),
        ('اطلاعات بیشتر', {
            'fields': ('ip', 'verify_code')
        }),

    ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ عضویت'

    def select_users_for_sms(self, request, queryset):
        current_domain = get_current_site(request).domain
        if 'apply' in request.POST:
            sms_obj = SendSMS.objects.create()
            sms_obj.recipients.add(*queryset)
            sms_obj.save()
            return HttpResponseRedirect(request.get_full_path())
        context = {
            'users': queryset,
            'domain': current_domain
        }
        return render(request, 'admin/select_users.html', context)

    def has_view_permission(self, request, obj=None):
        if request.user.is_staff:
            return True

    select_users_for_sms.short_description = _('انتخاب کاربران جهت ارسال پیامک')


@admin.register(models.ProfileCompletionPoints)
class ProfileCompletionPointsAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        related_per = 'accounts.add_profilecompletionpoints'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.change_profilecompletionpoints'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.view_profilecompletionpoints'
        return role_permission_checker(related_per, request.user)


@admin.register(models.ActivityPoint)
class ActivityPointsAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        related_per = 'accounts.add_activitypoint'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'accounts.add_activitypoint'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'accounts.add_activitypoint'
        return role_permission_checker(related_per, request.user)


@admin.register(models.AppUpdate)
class AppUpdateAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

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


admin.site.unregister(Group)
