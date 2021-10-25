from django.core import exceptions
from django.contrib.auth.views import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Ticket, Answer

User = get_user_model()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['ticket', 'text']

    def save(self, **kwargs):
        user = kwargs['user']
        answer = Answer.objects.create(user=user, ticket=self.validated_data.get('ticket'),
                                       text=self.validated_data.get('text'), seen_user=kwargs['seen_user'],
                                       seen_admin=kwargs['seen_admin'])

        return answer


class AnswerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'text', 'seen_user', 'seen_admin', 'created_at']


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'topic',
            'section',
            'request_text',
            'file',
            'status',
            'created_at',
        ]

    def save(self, **kwargs):
        ticket = Ticket.objects.create(user=kwargs['user'], topic=self.validated_data.get('topic'),
                                       section=self.validated_data.get('section'),
                                       request_text=self.validated_data.get('request_text'),
                                       file=self.validated_data.get('file'), )
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
