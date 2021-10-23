from django.contrib import admin
from . import models


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'topic', 'status', 'created_at', ]

    list_editable = ['status']
    list_filter = ['user', 'status', 'created_at']


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'seen_user', 'seen_admin', 'created_at']
    list_editable = ['seen_admin', 'seen_user']
    list_filter = ['seen_admin', 'seen_user']
