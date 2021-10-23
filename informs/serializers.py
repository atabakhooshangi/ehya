from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Inform

User = get_user_model()


class InformSerializer(serializers.ModelSerializer):
    recipients = serializers.SerializerMethodField()
    classification = serializers.SerializerMethodField()

    class Meta:
        model = Inform
        fields = ['recipients', 'topic', 'text', 'classification', 'created_at']

    def get_recipients(self, obj):
        return obj.get_recipients_display()

    def get_classification(self, obj):
        return obj.get_classification_display()
