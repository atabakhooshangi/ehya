from django.urls import path
from .views import SupportTicketAPIView, GetUserSupportTicketsAPIView, SupportAnswerAPIView, RetrieveTicketSerializer, \
    SupportSectionAPIView, seen_by_user, status_api_support, support_ticket_count_api

app_name = 'Support'

urlpatterns = [
    path('create_support_ticket', SupportTicketAPIView.as_view(), name='Create-Support-Ticket'),
    path('get_support_tickets', GetUserSupportTicketsAPIView.as_view(), name='Get-Support-Tickets'),
    path('create_support_answer', SupportAnswerAPIView.as_view(), name='Create-Support-Answer'),
    path('retreive_support_ticket', RetrieveTicketSerializer.as_view(), name='Retrieve-Support-Ticket'),
    path('support_section', SupportSectionAPIView.as_view(), name='Support-Section'),
    path('answer_seen', seen_by_user, name='Answer-Seen'),
    path('statuses_support', status_api_support, name='Support-Status'),
    path('support_ticket_count_', support_ticket_count_api, name='Support-Ticket-Count'),

]
