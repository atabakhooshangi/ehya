# Internal imports
from .models import Ticket, TicketPointCost, Section
from .serializers import TicketGetSerializer, AnswerSerializer, TicketCreateSerializer, SectionSerializer
from .permissions import is_expert, IsOwner, IsExpert
from accounts.renderers import Renderer, SimpleRenderer

# Django imports
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

User = get_user_model()


class TicketAPIView(CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [SimpleRenderer]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)


class AnswerAPIView(generics.GenericAPIView):
    serializer_class = AnswerSerializer
    renderer_classes = [SimpleRenderer]
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsExpert]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        if is_expert(self.request.user):
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user, ticket_id=data['ticket'], text=data['text'], file=data['file'])
            return Response(status=HTTP_201_CREATED)
        return Response({'user': _('اجازه این عملیات را ندارید')}, HTTP_403_FORBIDDEN)


class GetUserTicketsAPIView(generics.ListAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketGetAPIView(generics.ListAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.all()


class RetrieveATicketAPIView(generics.RetrieveAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        obj = get_object_or_404(Ticket, id=self.kwargs['pk'])
        return obj


class SectionListApiView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]
    renderer_classes = [Renderer]
    queryset = Section.objects.all()
