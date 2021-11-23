from django.utils.translation import ugettext as _
from .serializers import InformSerializer
from .models import Inform
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.renderers import Renderer

User = get_user_model()


class GetInformsAPIView(generics.ListAPIView):
    serializer_class = InformSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        inf_type = self.kwargs['inform_type']
        if inf_type == 'public':
            return Inform.objects.filter(inf_type='2')
        if inf_type == 'personal':
            return Inform.objects.filter(inf_type='1', user=self.request.user)
        if inf_type == 'roles':
            return Inform.objects.filter(inf_type='3', roles=self.request.user.role)
