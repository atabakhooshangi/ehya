from django.core import exceptions
from django.contrib.auth.views import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from jalali_date import datetime2jalali, date2jalali
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Ticket, Answer, TicketPointCost, Section, TicketAnswerLimit
from .permissions import is_expert

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    ticket = serializers.CharField(max_length=255)
    base_64_file = serializers.CharField(required=False)

    class Meta:
        model = Answer
        fields = ['ticket', 'text', 'base_64_file']

    def validate(self, attrs):
        try:
            Ticket.objects.get(id=int(attrs.get('ticket')))
        except Exception:
            raise serializers.ValidationError({'ticket': _('تیکت وارد شده وجود ندارد')})
        # else:
        #     if not is_expert(self.context.get('request').user):
        #         raise PermissionDenied({'user': _('اجازه این عملیات را ندارید')})

        return attrs

    def save(self, **kwargs):
        if 'base_64_file' in self.validated_data:
            f_format, imgstr = self.validated_data.get('base_64_file').split(';base64,')
            ext = f_format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            data = None
        user = kwargs['user']
        answer = Answer.objects.create(user=user, ticket_id=int(self.validated_data['ticket']),
                                       text=self.validated_data['text'],
                                       file=data)

        return answer


class AnswerGetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['user', 'text', 'file', 'created_at']

    def get_user(self, obj):
        ticket_user = self.context.get("ticket_user")
        if obj.user.id == ticket_user:
            return 'کاربر'
        return 'کارشناس'

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')


class TicketCreateSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField(read_only=True)
    section_id = serializers.CharField(max_length=10, write_only=True)
    base_64_file = serializers.CharField(required=False)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'topic',
            'section',
            'section_id',
            'request_text',
            'base_64_file',
            'status',
            'created_at',
        ]

    def get_section(self, obj):
        section = get_object_or_404(Section, id=int(obj['section_id']))
        return section.name

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user.check_point_status_for_ticket:
            return attrs
        raise serializers.ValidationError({'points': _('شما دارای امتیاز کافی جهت طرح پرسش  نمی باشید')})

    def save(self, **kwargs):
        user = kwargs['user']
        if 'base_64_file' in self.validated_data:
            f_format, imgstr = self.validated_data.get('base_64_file').split(';base64,')
            ext = f_format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            data = None
        section = get_object_or_404(Section, id=int(self.validated_data.get('section_id')))
        ticket = Ticket.objects.create(user=user, topic=self.validated_data.get('topic'),
                                       section=section,
                                       request_text=self.validated_data.get('request_text'),
                                       file=data)
        if user.check_point_status_for_ticket:
            user.points -= TicketPointCost.objects.last().value
            user.save()
        return ticket


class TicketGetSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'topic',
            'section',
            'request_text',
            'file',
            'status',
            'created_at',
            'answers'
        ]

    def get_answers(self, obj):
        return AnswerGetSerializer(obj.answer_set.all(), many=True, context={'ticket_user': obj.user.id}).data

    def get_status(self, obj):
        return obj.get_status_display()

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']
