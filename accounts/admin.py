from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'role', 'is_active', 'is_admin', 'is_staff', 'is_superuser',
                    'date_joined']
    list_editable = ['role', 'is_active', 'is_admin', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_active', 'is_admin', 'is_staff', 'is_superuser']


admin.site.unregister(Group)
