from django.urls import path
from .views import TicketAPIView, AnswerAPIView, RetrieveATicketAPIView, SectionListApiView, \
    TicketGetAPIView, close_ticket, reference_to_senior_expert

app_name = 'Tickets'

urlpatterns = [
    path('create_ticket', TicketAPIView.as_view(), name='Create-Ticket'),
    path('close_ticket/<int:ticket_id>', close_ticket, name='Close-Ticket'),
    path('reference_ticket/<int:ticket_id>', reference_to_senior_expert, name='Reference-Ticket'),
    path('create_answer', AnswerAPIView.as_view(), name='Create-Answer'),
    # path('get_user_tickets', GetUserTicketsAPIView.as_view(), name='User-Tickets'),
    path('get_tickets', TicketGetAPIView.as_view(), name='User-Tickets'),
    path('get_ticket', RetrieveATicketAPIView.as_view(), name='User-Tickets'),
    path('sections', SectionListApiView.as_view(), name='Sections'),
]
