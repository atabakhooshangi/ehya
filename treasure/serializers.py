from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404
import base64
from django.core.files.base import ContentFile
from .models import Treasury

User = get_user_model()


# Unsupported_Extensions = ['mkv', 'mp4', 'mov', 'wmv', 'avi', 'avchd', 'flv', 'f4v', 'swf', 'webm']

class GetTreasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treasury
        fields = ['id', 'user', 'topic', 'link', 'file']


class TreasureSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=40, read_only=True)
    base_64_file = serializers.CharField(required=False)

    class Meta:
        model = Treasury
        fields = ['id', 'user', 'topic', 'link', 'base_64_file']

    def validate(self, attrs):
        if 'base_64_file' in attrs:
            f_format, filestr = attrs.get('base_64_file').split(';base64,')
            extension = f_format.split('/')[-1]
            data = ContentFile(base64.b64decode(filestr), name='temp.' + extension)
            if data.size > 5242880:
                raise serializers.ValidationError(
                    {'file': 'فایل ارسالی نمیتواند بیشتر از 5 مگابایت باشد .'})
            attrs['base_64_file'] = data
        else:
            attrs['base_64_file'] = None
        return attrs

    def save(self, **kwargs):
        return Treasury.objects.create(user=kwargs['user'], topic=self.validated_data['topic'],
                                       link=self.validated_data['link'], file=self.validated_data['base_64_file'])
