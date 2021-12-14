from django.urls import path
from .views import TicketAPIView, AnswerAPIView, RetrieveATicketAPIView, SectionListApiView, \
    TicketGetAPIView, close_ticket, reference_to_senior_expert, seen_by_user

app_name = 'Tickets'

urlpatterns = [
    path('create_ticket', TicketAPIView.as_view(), name='Create-Ticket'),
    path('close_ticket', close_ticket, name='Close-Ticket'),
    path('reference_ticket', reference_to_senior_expert, name='Reference-Ticket'),
    path('answer_seen', seen_by_user, name='Answer-Seen'),
    path('create_answer', AnswerAPIView.as_view(), name='Create-Answer'),
    # path('get_user_tickets', GetUserTicketsAPIView.as_view(), name='User-Tickets'),
    path('get_tickets', TicketGetAPIView.as_view(), name='User-Tickets'),
    path('get_ticket', RetrieveATicketAPIView.as_view(), name='User-Tickets'),
    path('sections', SectionListApiView.as_view(), name='Sections'),
]
