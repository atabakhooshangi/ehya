from django.contrib import admin
from . import models


@admin.register(models.Inform)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipients', 'classification', 'topic', 'user', 'created_at', ]

    list_editable = ['classification','recipients']
    list_filter = ['recipients', 'classification', 'created_at']
