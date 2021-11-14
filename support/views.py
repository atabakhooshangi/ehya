# Internal imports
from .models import SupportTicket
from .serializers import SupportTicketSerializer
from ticket.permissions import is_expert, IsOwner, IsExpert, IsExpertOrIsOwner
from accounts.renderers import Renderer, SimpleRenderer

# Django imports
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.decorators import api_view, permission_classes, authentication_classes, renderer_classes
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

User = get_user_model()


class SupportTicketAPIView(generics.CreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [SimpleRenderer]

    def perform_create(self, serializer):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)


class GetUserSupportTicketsAPIView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)
