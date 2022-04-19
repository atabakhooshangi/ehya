from django.conf import settings
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from django.template.defaultfilters import truncatechars

from accounts.models import PointGainHistory, AppSettings
from ehyasalamat.permission_check import role_permission_checker
from .admin_filter import CommentApprovedFilter, PostCategoryFilter, InformsInfTypeSerializer
from .models import Post, Category, Tag, Comment, upload_thumbnail_location
from push_notification.main import PushThread
from django.utils.translation import ugettext as _
from django.contrib.flatpages.models import FlatPage
from django.urls import reverse
from tinymce.widgets import TinyMCE


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0
    autocomplete_fields = ['user', 'related_post']
    readonly_fields = ['date_created']
    fields = ['text', 'user', 'parent', 'approved', 'date_created']

    def has_add_permission(self, request, obj=None):
        related_per = 'wphome.add_comment'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'wphome.change_comment'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'wphome.view_comment'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'wphome.delete_comment'
        return role_permission_checker(related_per, request.user)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # List display customization
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/wphome/post/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/wphome/post/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')

    def truncated_short_desc(self, obj):
        return truncatechars(obj.short_description, 75)

    def truncated_desc(self, obj):
        return truncatechars(obj.description, 75)

    truncated_desc.short_description = _('متن مطلب')
    def categories_name(self, obj):
        cat_list = []
        categories = obj.categories.all()
        for category in categories:
            cat_list.append(category.name)

        output = ' , '.join(cat_list)
        return output

    def audio_preview(self, obj):
        if obj.file:
            return mark_safe(
                f'<audio controls><source src={obj.file.url} preload="auto" type="audio/mpeg">فایل ساپورت نمیشود</audio>')
        return "موردی یافت نشد"

    audio_preview.short_description = 'پیش نمایش صوت'

    list_display = ['change_button', 'title', 'truncated_desc','truncated_short_desc', 'categories_name', 'status', 'delete_button']
    filter_horizontal = ['tags', 'likes', 'views', 'favorite', 'categories']
    search_fields = ['title', 'categories__name', 'tags__name']
    list_filter = [PostCategoryFilter, InformsInfTypeSerializer]
    inlines = [CommentInLine]
    readonly_fields = (
        'thumbnail_preview', 'get_likes_count', 'get_views_count', 'get_favorite_count', 'date_created',
        'audio_preview','id')
    fieldsets = [
        ('وارد کردن عناوین و متون پست', {
            'fields': (
                'id','title', 'categories', "short_description", "description", "share_link",)}),
        ('تصویر پست', {
            'fields': (
                'image', 'thumbnail_preview',)}),
        ('رادیو احیا', {
            'fields': ('file', 'radio_ehya', 'audio_preview')
        }),
        ('احیا تی وی', {
            'fields': ('link_tv', 'ehya_tv',)
        }),
        ('تنظیمات پوش نوتیفیکیشن', {
            'fields': ('push_notif_description', 'push_notif_thumbnail', 'send_push',)
        }),
        ('برچسب ها', {
            'fields': ('tags',)
        }),
        ('آمار لایک', {
            'fields': ('likes', 'get_likes_count',)
        }),
        ('آمار بازدید', {
            'fields': ('views', 'get_views_count',)
        }),
        ('آمار علاقه مندی', {
            'fields': ('favorite', 'get_favorite_count',)
        }),
        ('وضعیت و زمان انتشار', {
            'fields': ('status', 'date_to_publish', 'date_created','special_post')
        }),
    ]

    truncated_short_desc.short_description = _('خلاصه مطلب')
    categories_name.short_description = _('دسته بندی ها')

    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_views_count(self, obj):
        return obj.views.all().count()

    def get_favorite_count(self, obj):
        return obj.favorite.all().count()

    get_likes_count.short_description = _('تعذاد لایک ها')
    get_views_count.short_description = _('تعداد بازدیدها')
    get_favorite_count.short_description = _('تعداد علاقه مندها')

    # Tiny MCE

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'short_description' or db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'پیش نمایش'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            if instance.approved is True:
                if instance.point_gained is False:
                    comment_point_gain = AppSettings.objects.last()
                    instance.user.points += comment_point_gain.comment_point
                    instance.point_gained = True
                    instance.user.save()
                    instance.save()
                    PointGainHistory.objects.create(user=instance.user,
                                                    action=f'درج کامنت در پست',
                                                    point=comment_point_gain.comment_point)

        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        photo_url = upload_thumbnail_location(obj, str(obj.push_notif_thumbnail))
        url = 'http://' + get_current_site(request).domain + settings.MEDIA_URL + photo_url
        if obj.send_push and obj.status != '5':
            PushThread(section='home', title=obj.title, body=obj.push_notif_description,
                       push_type='all',
                       image=str(url)).start()
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    # List display customization
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/wphome/category/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/wphome/category/{}/delete/">حذف</a>',
            obj.id)

    def icon_preview(self, obj):
        return obj.icon_preview

    readonly_fields = ['icon_preview','id']
    icon_preview.short_description = 'پیش نمایش'
    fieldsets = [
        (' ', {
            'fields': (
                'id','name', 'icon', 'icon_preview', "code_1", "code_2", "text_color", "parent",)}), ]
    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'name', 'parent', 'delete_button']
    autocomplete_fields = ['parent']
    search_fields = ['parent', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/wphome/tag/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/wphome/tag/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')
    list_display = ['change_button', 'name', 'delete_button']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):

    # List display customization
    def change_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/wphome/comment/{}/change/">ویرایش</a>',
            obj.id)

    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color:red;" href="/admin/wphome/comment/{}/delete/">حذف</a>',
            obj.id)

    change_button.short_description = _('ویرایش')
    delete_button.short_description = _('حذف')

    def short_description(self, obj):
        return truncatechars(obj.text, 55)

    def parent_short_description(self, obj):
        if obj.parent:
            return truncatechars(obj.parent.text, 55)
        return "---"

    list_display = ['change_button', 'user', 'short_description', 'parent_short_description', 'approved',
                    'delete_button']
    actions = ['approve_multiple_comments']
    list_filter = [CommentApprovedFilter]
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']

    # TinyMCE

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    # fieldsets
    def parent_text(self, obj):
        return obj.parent.text

    parent_text.short_description = _('متن کامنت والد')
    readonly_fields = ['parent_text']
    fieldsets = [
        ('کاربر', {
            'fields': (
                'user',)}),
        ('پست مرتبط', {
            'fields': (
                'related_post',)}),
        ('کامت والد', {
            'fields': ('parent', 'parent_text',)
        }),
        ('متن کامنت', {
            'fields': ('text', 'approved', 'point_gained')
        }),
    ]

    short_description.short_description = _('خلاصه کامنت')
    parent_short_description.short_description = _('خلاصه کامنت والد')

    # Actions
    def approve_multiple_comments(self, request, queryset):
        current_domain = get_current_site(request).domain
        if 'apply' in request.POST:
            for cm in queryset:
                cm.approved = True
                if not cm.point_gained:
                    comment_point_gain = AppSettings.objects.last()
                    cm.user.points += comment_point_gain.comment_point
                    cm.user.save()
                    cm.point_gained = True
                    PointGainHistory.objects.create(user=cm.user,
                                                    action=f'درج کامنت در پست',
                                                    point=comment_point_gain.comment_point)
                cm.save()
            return HttpResponseRedirect(request.get_full_path())
        context = {
            'comments': queryset,
            'domain': current_domain
        }
        return render(request, 'admin/select_comments.html', context)

    approve_multiple_comments.short_description = _('تایید کامنت های انتخاب شده')

    def save_model(self, request, obj, form, change):
        if obj.approved:
            if not obj.point_gained:
                comment_point_gain = AppSettings.objects.last()
                obj.user.points += comment_point_gain.comment_point
                obj.point_gained = True
                PointGainHistory.objects.create(user=obj.user,
                                                action=f'درج کامنت در پست',
                                                point=comment_point_gain.comment_point)
                obj.user.save()
        super().save_model(request, obj, form, change)


admin.site.unregister(FlatPage)
