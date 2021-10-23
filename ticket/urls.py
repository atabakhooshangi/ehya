from django.urls import path
from .views import TicketAPIView, AnswerAPIView, TicketGetAPIView, RetrieveATicketAPIView

app_name = 'Tickets'

urlpatterns = [
    path('create-ticket', TicketAPIView.as_view(), name='Create-Ticket'),
    path('create-answer', AnswerAPIView.as_view(), name='Create-Answer'),
    path('get-tickets', TicketGetAPIView.as_view(), name='User-Tickets'),
    path('get-ticket/<int:pk>', RetrieveATicketAPIView.as_view(), name='User-Tickets'),
]
