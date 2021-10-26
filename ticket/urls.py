from django.urls import path
from .views import TicketAPIView, AnswerAPIView, TicketGetAPIView, RetrieveATicketAPIView

app_name = 'Tickets'

urlpatterns = [
    path('create_ticket', TicketAPIView.as_view(), name='Create-Ticket'),
    path('create_answer', AnswerAPIView.as_view(), name='Create-Answer'),
    path('get_tickets', TicketGetAPIView.as_view(), name='User-Tickets'),
    path('get_ticket/<int:pk>', RetrieveATicketAPIView.as_view(), name='User-Tickets'),
]
