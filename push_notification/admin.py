from django.contrib import admin
from .models import PushNotificationSections


@admin.register(PushNotificationSections)
class PushNotifAdmin(admin.ModelAdmin):
    list_display = ['id', 'home', 'support', 'ticket', 'treasure', 'inform']
    list_editable = ['home', 'support', 'ticket', 'treasure', 'inform']

    def has_add_permission(self, request):
        related_per = 'push_notification.add_pushnotificationsections'
        if self.model.objects.count() >= 1:
            return False
        elif self.model.objects.count() < 1 and related_per in request.user.get_user_permissions():
            return True

    def has_change_permission(self, request, obj=None):
        related_per = 'push_notification.add_pushnotificationsections'
        if related_per in request.user.get_user_permissions():
            return True

    def has_view_permission(self, request, obj=None):
        related_per = 'push_notification.add_pushnotificationsections'
        if related_per in request.user.get_user_permissions():
            return True
