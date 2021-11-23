from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Inform

User = get_user_model()


class InformSerializer(serializers.ModelSerializer):
    classification = serializers.SerializerMethodField()
    inf_type = serializers.SerializerMethodField()

    class Meta:
        model = Inform
        fields = ['inf_type', 'topic', 'text', 'classification', 'created_at']

    def get_inf_type(self, obj):
        return obj.get_inf_type_display()

    def get_classification(self, obj):
        return obj.get_classification_display()
