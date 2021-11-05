from django.core import exceptions
from django.contrib.auth.views import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Ticket, Answer, TicketPointCost, Section
from .permissions import is_expert

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    ticket = serializers.CharField(max_length=255)

    class Meta:
        model = Answer
        fields = ['ticket', 'text', 'file']

    def validate(self, attrs):
        try:
            Ticket.objects.get(id=int(attrs.get('ticket')))
        except:
            raise serializers.ValidationError({'ticket': _('تیکت وارد شده وجود ندارد')})
        else:
            if not is_expert(self.context.get('request').user):
                raise PermissionDenied({'user': _('اجازه این عملیات را ندارید')})
        return attrs

    def save(self, **kwargs):
        user = kwargs['user']
        ticket_id = kwargs['ticket_id']
        text = kwargs['text']
        file = kwargs['file']
        answer = Answer.objects.create(user=user, ticket_id=ticket_id, text=text, file=file)

        return answer


class AnswerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'text', 'file', 'created_at']


class TicketCreateSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField(read_only=True)
    section_id = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = Ticket
        fields = [
            'topic',
            'section',
            'section_id',
            'request_text',
            'file',
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
        section = get_object_or_404(Section, id=int(self.validated_data.get('section_id')))
        ticket = Ticket.objects.create(user=user, topic=self.validated_data.get('topic'),
                                       section=section,
                                       request_text=self.validated_data.get('request_text'),
                                       file=self.validated_data.get('file'))
        if user.check_point_status_for_ticket:
            user.points -= TicketPointCost.objects.last().value
            user.save()
        return ticket


class TicketGetSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'topic',
            'section',
            'request_text',
            'file',
            'status',
            'created_at',
            'answers'
        ]

    def get_answers(self, obj):
        return AnswerGetSerializer(obj.answer_set.all(), many=True).data


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']
