from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
from .models import Treasury

User = get_user_model()

Unsupported_Extensions = ['mkv', 'mp4', 'mov', 'wmv', 'avi', 'avchd', 'flv', 'f4v', 'swf', 'webm']


class TreasureSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Treasury
        fields = ['id', 'user', 'topic', 'link', 'file']

    def validate(self, attrs):
        extension = str(attrs['file']).split('.')[-1]

        if extension in Unsupported_Extensions:
            raise serializers.ValidationError({'file': 'فایل ارسالی نمیتواند ویدئو باشد . فقط تصویر و صوت مجاز است.'})
        return attrs

    def save(self, **kwargs):
        return Treasury.objects.create(user=kwargs['user'], topic=self.validated_data['topic'],
                                       link=self.validated_data['link'], file=self.validated_data['file'])
