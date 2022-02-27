from django.contrib import admin

from accounts.models import User
from ehyasalamat.permission_check import role_permission_checker
from .main import PushThread
from .models import PushNotificationSections, SendPush


@admin.register(PushNotificationSections)
class PushNotifAdmin(admin.ModelAdmin):
    list_display = ['id', 'home', 'support', 'ticket', 'inform']
    list_editable = ['home', 'support', 'ticket', 'inform']

    def has_add_permission(self, request):
        related_per = 'push_notification.add_pushnotificationsections'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and role_permission_checker(related_per, request.user):
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'push_notification.change_pushnotificationsections'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.view_pushnotificationsections'
        return role_permission_checker(related_per, request.user)


@admin.register(SendPush)
class SendPushAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'date_created']

    def has_add_permission(self, request):
        related_per = 'push_notification.add_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_change_permission(self, request, obj=None):
        related_per = 'push_notification.change_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.view_sendpush'
        return role_permission_checker(related_per, request.user)

    def has_delete_permission(self, request, obj=None):
        related_per = 'push_notification.delete_sendpush'
        return role_permission_checker(related_per, request.user)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.send_to_all:
            PushThread(section='push', title=obj.title, body=obj.body, image=obj.image,
                       push_type='all').start()
        else:
            obj.receptors.clear()
            users = form.cleaned_data['receptors']
            PushThread(section='push', title=obj.title, body=obj.body, image=obj.image,
                       push_type='group', user=users).start()
