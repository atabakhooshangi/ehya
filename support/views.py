# Internal imports
from .models import SupportTicket, SupportSection
from .serializers import SupportTicketSerializer, GetSupportTicketSerializer, SupportAnswerSerializer
from .utils import reached_support_answer_limit
from ticket.permissions import is_expert, IsOwner, IsExpert, IsExpertOrIsOwner
from accounts.renderers import Renderer, SimpleRenderer
from .permissions import IsSupportAdminOrOwner
# Django imports
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.decorators import api_view, permission_classes
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
    serializer_class = GetSupportTicketSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]

    def get_queryset(self):
        if self.request.user.is_support:
            section = SupportSection.objects.filter(associated_roles__in=[self.request.user.role]).last()
            if self.request.user.role.is_expert:
                return SupportTicket.objects.filter(section=section)
            return SupportTicket.objects.filter(section=section).exclude(status='2')
        return SupportTicket.objects.filter(user=self.request.user)


class SupportAnswerAPIView(generics.GenericAPIView):
    serializer_class = SupportAnswerSerializer
    permission_classes = [IsSupportAdminOrOwner]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        supp_ticket_obj = SupportTicket.objects.get(id=data['ticket'])
        self.check_object_permissions(request=request, obj=supp_ticket_obj)
        if reached_support_answer_limit(user=request.user, obj=supp_ticket_obj):
            if supp_ticket_obj.status == '1':
                supp_ticket_obj.status = '3'
                supp_ticket_obj.save()
            serializer.save(user=self.request.user)
            return Response({'isDone': True}, status=HTTP_201_CREATED)
        return Response({'isDone': False, 'data': [{
            'error': 'شما به حداکثر تعداد مجاز پاسخ به سوال رسیده اید. لطفا پرسش جدیدی ایجاد کرده و موضوع خود را به کارشناسان پشتیبانی ما مطرح کنید.  '}]},
                        status=HTTP_400_BAD_REQUEST)


class RetrieveTicketSerializer(generics.RetrieveAPIView):
    serializer_class = GetSupportTicketSerializer
    permission_classes = [IsSupportAdminOrOwner]

    def get_object(self):
        obj = get_object_or_404(SupportTicket, id=self.kwargs['pk'])
        self.check_object_permissions(request=self.request, obj=obj)
        return obj


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_support_ticket(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        if request.user.role in ticket.section.associated_roles.all():
            ticket.status = '5'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reference_to_senior_support(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        if request.user.role in ticket.section.associated_roles.all():
            ticket.status = '2'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)
