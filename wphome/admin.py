from django.contrib import admin

from .models import WpPosts, WpComments


@admin.register(WpPosts)
class WpPostsAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(WpComments)
class WpCommentsAdmin(admin.ModelAdmin):
    list_display = ['id']
