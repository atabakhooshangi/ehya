# Internal imports
from .models import Ticket, TicketPointCost, Section
from .serializers import TicketGetSerializer, AnswerSerializer, TicketCreateSerializer, SectionSerializer
from .permissions import is_expert, IsOwner, IsExpert, IsExpertOrIsOwner
from accounts.renderers import Renderer, SimpleRenderer
from .utils import reached_answer_limit

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


class TicketAPIView(CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]
    parser_classes = (MultiPartParser, FormParser)

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
        if reached_answer_limit(user=request.user, obj=ticket_obj):
            if ticket_obj.status == '1':
                ticket_obj.status = '3'
                ticket_obj.save()
            serializer.save(user=self.request.user, ticket_id=data['ticket'], text=data['text'], file=data['file'])
            return Response({'isDone': True}, status=HTTP_201_CREATED)
        return Response({'isDone': False, 'data': [{
            'error': 'شما به حداکثر تعداد مجاز پاسخ به سوال رسیده اید. لطفا پرسش جدیدی ایجاد کرده و موضوع خود را به کارشناسان ما مطرح کنید.  '}]},
                        status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def close_ticket(request, ticket_id):
    if request.method == 'POST':
        if request.user.role.name in ['کارشناس', 'کارشناس ارشد']:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.status = '4'
            ticket.save()
            return Response({'isDone': True}, status=HTTP_200_OK)
        return Response({'isDone': False}, status=HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reference_to_senior_expert(request, ticket_id):
    if request.method == 'POST':
        if request.user.role.name == 'کارشناس':
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.status = '2'
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
        if self.request.user.role.name in ['کارشناس', 'کارشناس ارشد']:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)


class RetrieveATicketAPIView(generics.RetrieveAPIView):
    serializer_class = TicketGetSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsExpertOrIsOwner]
    lookup_field = 'id'

    def get_object(self):
        obj = get_object_or_404(Ticket, id=self.kwargs['pk'])
        self.check_object_permissions(request=self.request, obj=obj)
        return obj


class SectionListApiView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]
    renderer_classes = [Renderer]
    queryset = Section.objects.all()
