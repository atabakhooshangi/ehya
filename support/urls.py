from django.urls import path
from .views import SupportTicketAPIView, GetUserSupportTicketsAPIView

app_name = 'Support'

urlpatterns = [
    path('create-support-ticket', SupportTicketAPIView.as_view(), name='Create-Support-Ticket'),
    path('get-support-tickets', GetUserSupportTicketsAPIView.as_view(), name='Get-Support-Tickets'),

]
