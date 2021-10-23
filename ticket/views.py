# Internal imports
from .models import Ticket
from .serializers import TicketSerializer, AnswerSerializer
from .permissions import is_owner, IsOwner

# Django imports
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

User = get_user_model()


class TicketAPIView(CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save(user=self.request.user)


class AnswerAPIView(generics.GenericAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        ticket = Ticket.objects.get(id=data['ticket'])
        serializer = self.serializer_class(data=data)
        if is_owner(obj=ticket, request_user=self.request.user):
            serializer.is_valid()
            serializer.save(user=self.request.user, seen_user=True, seen_admin=False)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if request.user.is_admin:
            serializer.is_valid()
            serializer.save(user=self.request.user, seen_user=False, seen_admin=True)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response({'user': _('اجازه این عملیات را ندارید')}, HTTP_403_FORBIDDEN)


class TicketGetAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class RetrieveATicketAPIView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get_object(self):
        obj = get_object_or_404(Ticket, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
