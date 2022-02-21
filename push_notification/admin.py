from django.contrib import admin

from ehyasalamat.permission_check import role_permission_checker
from .models import PushNotificationSections


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
        related_per = 'push_notification.add_pushnotificationsections'
        return role_permission_checker(related_per, request.user)

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.add_pushnotificationsections'
        return role_permission_checker(related_per, request.user)
