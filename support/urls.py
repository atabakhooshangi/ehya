from django.urls import path
from .views import SupportTicketAPIView, GetUserSupportTicketsAPIView, SupportAnswerAPIView, RetrieveTicketSerializer

app_name = 'Support'

urlpatterns = [
    path('create_support_ticket', SupportTicketAPIView.as_view(), name='Create-Support-Ticket'),
    path('get_support_tickets', GetUserSupportTicketsAPIView.as_view(), name='Get-Support-Tickets'),
    path('create_support_answer', SupportAnswerAPIView.as_view(), name='Create-Support-Answer'),
    path('retreive_support_ticket/<int:pk>', RetrieveTicketSerializer.as_view(), name='Retrieve-Support-Ticket'),

]
