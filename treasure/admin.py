from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from ehyasalamat.permission_check import role_permission_checker
from . import models
from jalali_date import datetime2jalali, date2jalali
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html
from django.contrib import admin


@admin.register(models.Treasury)
class TreasuryAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/treasure/treasury/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/treasure/treasury/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'user', 'topic', 'link_url', 'file_link', 'get_created_jalali', 'delete_button']
    list_filter = [('created_at', DateRangeFilter)]
    search_fields = ['topic', 'user__phone_number', 'user__first_name', 'user__last_name']
    readonly_fields = ['audio_video_image_preview']

    def audio_video_image_preview(self, obj):
        if obj.file:
            if obj.file.name.endswith(('.ogg', '.webm', '.mp4')):
                return mark_safe(
                    f'<video width="320" height="240" controls><source src={obj.file.url} preload="auto" type="video/mp4">فایل ساپورت نمیشود</video>')
            if obj.file.name.endswith(('.ogg', '.mp3', '.wav')):
                return mark_safe(
                    f'<audio controls><source src={obj.file.url} preload="auto" type="audio/mpeg">فایل ساپورت نمیشود</audio>')

            if obj.file.name.endswith(('.jpeg', '.png', '.svg', 'webp')):
                return mark_safe('<img src="{}" width="280" height="200" />'.format(obj.file.url))
            return ""

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
    audio_video_image_preview.short_description = 'پیش نمایش فایل'

    def has_add_permission(self, request, obj=None):
        related_per = 'treasure.add_treasury'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'treasure.change_treasury'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'treasure.view_treasury'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'treasure.delete_treasury'
        return role_permission_checker(related_per, request.user)


@admin.register(models.TreasureAnswer)
class TreasureAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_editable = ['text']

    def has_add_permission(self, request):
        related_per = 'treasure.change_treasureanswer'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'treasure.change_treasureanswer'
        return role_permission_checker(related_per, request.user)
