from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
# from jet.filters import RelatedFieldAjaxListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 0
    autocomplete_fields = ['user']
    readonly_fields = ['user']
    fields = ['text', 'file', 'status', 'user']

    def has_view_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_change_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_add_permission(self, request, obj):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'topic', 'status_for_user', 'status_for_expert', 'file_link', 'get_created_jalali', ]
    autocomplete_fields = ['user']
    list_editable = ['status_for_user', 'status_for_expert']
    list_filter = ['user', 'status_for_user', 'status_for_expert', 'created_at']
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

    def has_view_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_change_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_add_permission(self, request):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True

    inlines = [AnswerInLine]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'get_created_jalali']
    list_filter = [('created_at', DateRangeFilter)]
    autocomplete_fields = ['user']
    search_fields = ['user__phone_number']
    raw_id_fields = ['user']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = 'تاریخ ایجاد'

    def has_view_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_change_permission(self, request, obj=None):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_add_permission(self, request):
        if request.user.role:
            if request.user.is_staff and request.user.role.name in ['کارشناس', 'کارشناس ارشد'] or request.user.is_admin:
                return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True


@admin.register(models.TicketPointCost)
class TicketPointCostAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


@admin.register(models.TicketAnswerLimit)
class TicketAnswerLimitAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_editable = ['value']

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
