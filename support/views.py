# Internal imports
import datetime

from ehyasalamat.permission_check import support_permission_checker
from push_notification.main import PushThread
from .models import SupportTicket, SupportSection
from .serializers import SupportTicketSerializer, GetSupportTicketSerializer, SupportAnswerSerializer, \
    SupportSectionSerializer
from .utils import reached_support_answer_limit
from accounts.renderers import Renderer, SimpleRenderer
from .permissions import IsSupportAdminOrOwner

# Rest Framework imports
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from accounts.models import User


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
        if support_permission_checker(user=self.request.user):
            user_roles = self.request.user.role.all()
            section = SupportSection.objects.filter(associated_roles__in=user_roles)
            return SupportTicket.objects.filter(section__in=section)
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
            if request.user == supp_ticket_obj.user:
                supp_ticket_obj.status_for_user = '1'
                supp_ticket_obj.status_for_support = '4'
            else:
                supp_ticket_obj.status_for_user = '2'
                supp_ticket_obj.status_for_support = '2'
                user = User.objects.filter(id=supp_ticket_obj.user.id)
                PushThread(section='support', title=supp_ticket_obj.topic, body=data.get('text'),
                           push_type='personal', user=user).start()
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
        obj = get_object_or_404(SupportTicket, id=int(self.request.META['HTTP_ID']))
        self.check_object_permissions(request=self.request, obj=obj)
        return obj


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_support_ticket(request):
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, id=request.META['HTTP_ID'])
        bool_list = []
        for role in request.user.role.all():
            if role in ticket.section.associated_roles.all():
                bool_list.append('True')
        if 'True' in bool_list or request.user.is_superuser:
            ticket.status_for_user = '3'
            ticket.status_for_support = '3'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def reference_to_senior_support(request, ticket_id):
#     if request.method == 'POST':
#         ticket = get_object_or_404(SupportTicket, id=ticket_id)
#         if request.user.role in ticket.section.associated_roles.all():
#             ticket.status = '2'
#             ticket.save()
#             return Response({'isDone': True}, status=HTTP_200_OK)
#         return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


class SupportSectionAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SupportSectionSerializer
    renderer_classes = [Renderer]
    queryset = SupportSection.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seen_by_user(request):
    if request.method == 'POST':
        supp_ticket = get_object_or_404(SupportTicket, id=request.META['HTTP_ID'])
        if request.user == supp_ticket.user:
            answers = supp_ticket.supportanswer_set.filter(status='2')
            for answer in answers:
                answer.status = '1'
                answer.seen_at = datetime.datetime.now()
                answer.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


@api_view(['GET'])
@renderer_classes([Renderer])
@permission_classes([IsAuthenticated])
def status_api_support(request):
    if request.method == 'GET':
        if support_permission_checker(user=request.user):
            data = {
                '1': 'جدید',
                '3': 'پاسخ داده شده',
                '4': 'بسته شده',
                '5': 'پاسخ کاربر',
            }
            return Response(data, status=HTTP_200_OK)

        data = {
            '1': 'در حال بررسی',
            '2': 'پاسخ داده شده',
            '3': 'بسته شده'
        }
        return Response(data, status=HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([Renderer])
@permission_classes([IsAuthenticated])
def support_ticket_count_api(request):
    if request.method == 'GET':
        if support_permission_checker(user=request.user):
            new = SupportTicket.objects.filter(status_for_support='1').count()
            answered = SupportTicket.objects.filter(status_for_support='2').count()
            closed = SupportTicket.objects.filter(status_for_support='3').count()
            user_answer = SupportTicket.objects.filter(status_for_support='4').count()
            data = {
                'new': new,
                'answered': answered,
                'closed': closed,
                'user_answer': user_answer,
            }
            return Response(data, status=HTTP_200_OK)
        in_progress = SupportTicket.objects.filter(user=request.user, status_for_user='1').count()
        answered = SupportTicket.objects.filter(user=request.user, status_for_user='2').count()
        closed = SupportTicket.objects.filter(user=request.user, status_for_user='3').count()
        data = {
            'in_progress': in_progress,
            'answered': answered,
            'closed': closed
        }
        return Response(data, status=HTTP_200_OK)
