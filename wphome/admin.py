from django.conf import settings
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from mptt.admin import MPTTModelAdmin
from .models import Post, Category, Tag, Comment, CommentPoint, upload_thumbnail_location
from push_notification.main import PushThread


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0
    autocomplete_fields = ['user', 'related_post']
    readonly_fields = ['date_created']
    fields = ['text', 'user', 'parent', 'approved', 'date_created']

    def has_add_permission(self, request, obj=None):
        related_per = 'wphome.add_comment'
        if related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'wphome.change_comment'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'wphome.view_comment'
        if related_per in request.user.get_user_permissions():
            return True

    def has_delete_permission(self, request, obj=None):
        related_per = 'wphome.delete_comment'
        if related_per in request.user.get_user_permissions():
            return True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    filter_horizontal = ['tags']
    search_fields = ['user']
    inlines = [CommentInLine]

    def save_model(self, request, obj, form, change):
        photo_url = upload_thumbnail_location(obj, str(obj.push_notif_thumbnail))
        url = 'http://' + get_current_site(request).domain + settings.MEDIA_URL + photo_url
        if obj.send_push:
            PushThread(section='home', title=obj.title, body=obj.push_notif_description,
                       push_type='all',
                       image=str(url)).start()
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['id', 'name']
    autocomplete_fields = ['parent']
    search_fields = ['parent']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ['id', 'user']


@admin.register(CommentPoint)
class CommentPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']



