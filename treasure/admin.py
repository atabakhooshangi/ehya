from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html
from django.contrib import admin


@admin.register(models.Treasury)
class TreasuryAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'link_url', 'file_link', 'get_created_jalali']
    list_filter = [('created_at', DateRangeFilter)]
    search_fields = ['topic', 'user__phone_number']

    def file_link(self, obj):
        if obj.file:
            return format_html(f"<a href='{obj.file.url}' target='_blank'>مشاهده فایل</a>")
            # return format_html(f"<audio controls> <source src='{obj.file.url}'/>مشاهده فایل</audio>")
        return "فایلی آپلود نشده است"

    def link_url(self, obj):
        if obj.link:
            return format_html(f"<a href='{obj.link}' target='_blank'>{obj.link}</a>")
            # return format_html(f"<audio controls> <source src='{obj.file.url}'/>مشاهده فایل</audio>")
        return "---"

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'
    file_link.short_description = 'فایل آپلود شده'
    link_url.short_description = 'لینک'

    def has_add_permission(self, request, obj=None):
        related_per = 'treasure.add_treasury'
        if related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'treasure.change_treasury'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'treasure.view_treasury'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'treasure.delete_treasury'
        if related_per in request.user.get_user_permissions():
            return True


@admin.register(models.TreasureAnswer)
class TreasureAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_editable = ['text']

    def has_add_permission(self, request):
        related_per = 'treasure.change_treasureanswer'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        if related_per in request.user.get_user_permissions():
            return True
