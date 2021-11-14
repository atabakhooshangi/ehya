from django.core import exceptions
from django.contrib.auth.views import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['id', 'topic', 'request_text', 'status', 'created_at']

    def get_status(self, obj):
        request = self.context.get("request")
        if request.method == 'GET':
            return obj.get_status_display()
        return None

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
                                                  request_text=self.validated_data.get('request_text'))

        return sup_ticket
