# Internal imports
import datetime

from ehyasalamat.permission_check import ticket_permission_checker
from push_notification.main import PushThread
from .models import Ticket, Section
from .serializers import TicketGetSerializer, AnswerSerializer, TicketCreateSerializer, SectionSerializer
from .permissions import IsExpertOrIsOwner
from accounts.renderers import Renderer, SimpleRenderer
from .utils import not_reached_answer_limit

# Django imports
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

User = get_user_model()


class TicketAPIView(CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [SimpleRenderer]

    # parser_classes = (MultiPartParser, FormParser)0

    def perform_create(self, serializer):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)


class AnswerAPIView(generics.GenericAPIView):
    serializer_class = AnswerSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsExpertOrIsOwner]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ticket_obj = Ticket.objects.get(id=data['ticket'])
        self.check_object_permissions(request=request, obj=ticket_obj)
        if not_reached_answer_limit(user=request.user, obj=ticket_obj):
            if request.user == ticket_obj.user:
                ticket_obj.status_for_user = '1'
                ticket_obj.status_for_expert = '5'
            else:
                ticket_obj.status_for_user = '2'
                ticket_obj.status_for_expert = '3'
                user = User.objects.filter(id=ticket_obj.user.id)
                PushThread(section='ticket', title=ticket_obj.topic, body=data.get('text'),
                           push_type='personal', user=user).start()
            ticket_obj.save()
            serializer.save(user=self.request.user)
            return Response({'isDone': True}, status=HTTP_201_CREATED)
        return Response({'isDone': False, 'data': [{
            'error': 'شما به حداکثر تعداد مجاز پاسخ به سوال رسیده اید. لطفا پرسش جدیدی ایجاد کرده و موضوع خود را به کارشناسان ما مطرح کنید.  '}]},
                        status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_ticket(request):
    if request.method == 'POST':
        if ticket_permission_checker(user=request.user, role_list=['کارشناس', 'کارشناس ارشد']):
            ticket = get_object_or_404(Ticket, id=request.META['HTTP_ID'])
            ticket.status_for_user = '3'
            ticket.status_for_expert = '4'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reference_to_senior_expert(request):
    if request.method == 'POST':
        if ticket_permission_checker(user=request.user, role_list=['کارشناس']):
            ticket = get_object_or_404(Ticket, id=request.META['HTTP_ID'])
            ticket.status_for_user = '1'
            ticket.status_for_expert = '2'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


# class GetUserTicketsAPIView(generics.ListAPIView):
#     serializer_class = TicketGetSerializer
#     renderer_classes = [Renderer]
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Ticket.objects.filter(user=self.request.user)


class TicketGetAPIView(generics.ListAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if ticket_permission_checker(user=self.request.user, role_list=['کارشناس', 'کارشناس ارشد']):
            return Ticket.objects.all() if self.request.META['HTTP_FILTER'] == 'all' else Ticket.objects.filter(
                status_for_expert=self.request.META['HTTP_FILTER'])
        return Ticket.objects.filter(user=self.request.user) \
            if self.request.META['HTTP_FILTER'] == 'all' else Ticket.objects.filter(user=self.request.user,
                                                                                    status_for_user=self.request.META[
                                                                                        'HTTP_FILTER'])


class RetrieveATicketAPIView(generics.GenericAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsExpertOrIsOwner]

    def get_object(self):
        obj = get_object_or_404(Ticket, id=int(self.request.META['HTTP_TICKET']))
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=HTTP_200_OK)


class SectionListApiView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]
    renderer_classes = [Renderer]
    queryset = Section.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seen_by_user(request):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, id=request.META['HTTP_ID'])
        if request.user == ticket.user:
            answers = ticket.answer_set.filter(status='2')
            for answer in answers:
                if answer.user != request.user:
                    answer.status = '1'
                    answer.seen_at = datetime.datetime.now()
                    answer.save()
            return Response({'isDone': True}, status=HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([Renderer])
@permission_classes([IsAuthenticated])
def status_api(request):
    if request.method == 'GET':
        if ticket_permission_checker(user=request.user, role_list=['کارشناس', 'کارشناس ارشد']):
            data = {
                '1': 'جدید',
                '2': 'ارجاء به کارشناس ارشد',
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
def ticket_count_api(request):
    if request.method == 'GET':
        if ticket_permission_checker(user=request.user, role_list=['کارشناس', 'کارشناس ارشد']):
            new = Ticket.objects.filter(status_for_expert='1').count()
            refrenced = Ticket.objects.filter(status_for_expert='2').count()
            answered = Ticket.objects.filter(status_for_expert='3').count()
            closed = Ticket.objects.filter(status_for_expert='4').count()
            user_answer = Ticket.objects.filter(status_for_expert='5').count()
            data = {
                'جدید': new,
                'ارجاء به کارشناس ارشد': refrenced,
                'پاسخ داده شده': answered,
                'بسته شده': closed,
                'پاسخ کاربر': user_answer,
            }
            return Response(data, status=HTTP_200_OK)
        in_progress = Ticket.objects.filter(user=request.user, status_for_user='1').count()
        answered = Ticket.objects.filter(user=request.user, status_for_user='2').count()
        closed = Ticket.objects.filter(user=request.user, status_for_user='3').count()
        data = {
            'در حال بررسی': in_progress,
            'پاسخ داده شده': answered,
            'بسته شده': closed
        }
        return Response(data, status=HTTP_200_OK)
