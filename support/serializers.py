from django.core import exceptions
from django.contrib.auth.views import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import SupportTicket, SupportAnswer


class SupportAnswerGetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = SupportAnswer
        fields = ['user', 'ticket', 'text', 'created_at']

    def get_user(self, obj):
        ticket_user = self.context.get("ticket_user")
        if obj.user.id == ticket_user:
            return 'کاربر'
        return 'پشتیبان'

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')


class SupportTicketSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    section = serializers.CharField(max_length=20)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = SupportTicket
        fields = ['id', 'topic', 'section', 'request_text', 'status', 'created_at']

    def get_status(self, obj):
        request = self.context.get("request")
        if request.method == 'GET':
            return obj.get_status_display()
        return None

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if not user.profile_done:
            raise serializers.ValidationError(_('ابتدا باید پروفایل خود را تکمیل کنید.'))
        return attrs

    def save(self, **kwargs):
        user = kwargs['user']
        sup_ticket = SupportTicket.objects.create(user=user, topic=self.validated_data.get('topic'),
                                                  request_text=self.validated_data.get('request_text'),
                                                  section_id=int(self.validated_data['section']))

        return sup_ticket


class GetSupportTicketSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    section = serializers.CharField(max_length=20)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = SupportTicket
        fields = ['id', 'topic', 'section', 'request_text', 'status', 'created_at', 'answers']

    def get_status(self, obj):
        request = self.context.get("request")
        if request.method == 'GET':
            return obj.get_status_display()
        return None

    def get_answers(self, obj):
        return SupportAnswerGetSerializer(obj.supportanswer_set.all(), many=True,
                                          context={'ticket_user': obj.user.id}).data

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d _ %H:%M:%S')


class SupportAnswerSerializer(serializers.ModelSerializer):
    ticket = serializers.CharField(max_length=255)

    class Meta:
        model = SupportAnswer
        fields = ['ticket', 'text']

    def validate(self, attrs):
        try:
            SupportTicket.objects.get(id=int(attrs.get('ticket')))
        except Exception:
            raise serializers.ValidationError({'ticket': _('تیکت پشتیبانی وارد شده وجود ندارد')})

        return attrs

    def save(self, **kwargs):
        user = kwargs['user']
        answer = SupportAnswer.objects.create(user=user, ticket_id=int(self.validated_data['ticket']),
                                              text=self.validated_data['text'])

        return answer
