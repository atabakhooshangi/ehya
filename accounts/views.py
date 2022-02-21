import json
from django.utils.translation import ugettext as _
from rest_framework.decorators import api_view, permission_classes

from .renderers import Renderer
from .serializers import RegisterLoginSerializer, VerificationCodeSerializer, UserSerializer, ReferralSerializer, \
    RoleSerializer
import requests
from random import randint
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from .utils import get_visitor_ipaddress
from .models import ProfileCompletionPoints, Role, ActivityPoint, AppUpdate

User = get_user_model()


class RegisterLoginAPIView(generics.GenericAPIView):
    serializer_class = RegisterLoginSerializer
    renderer_classes = [Renderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data['phone_number']
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        code = randint(1000, 9999)
        obj = serializer.is_user()
        ip = get_visitor_ipaddress(request)
        if isinstance(obj, User):
            obj.verify_code = code
            obj.ip = ip
            obj.save()
            message = f'   کد احراز هویت شما : {code}'
            url = 'http://185.4.28.100/class/sms/restful/sendSms_OneToMany.php'

            params = {'uname': 'hakimdr', 'pass': '52b@4ED', 'from': '+985000171', 'to': [phone_number],
                      'msg': f'{message}'}

            response = requests.post(url, data=json.dumps(params))
            return Response(status=HTTP_200_OK)
        user = User.objects.create_user(phone_number=phone_number, password=None)
        user.ip = ip
        user.verify_code = code
        user.role.add(Role.objects.filter(name='عضو عادی').last())
        user.save()
        message = f'   کد احراز هویت شما : {code}'
        url = 'http://185.4.28.100/class/sms/restful/sendSms_OneToMany.php'

        params = {'uname': 'hakimdr', 'pass': '52b@4ED', 'from': '+985000171', 'to': [user.phone_number],
                  'msg': f'{message}'}

        response = requests.post(url, data=json.dumps(params))
        return Response(status=HTTP_201_CREATED)


class VerifyAuthenticationCodeAPIView(generics.GenericAPIView):
    serializer_class = VerificationCodeSerializer
    renderer_classes = [Renderer]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)


class UserProfileAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.profile_done and instance.profile_completion_point == '2':
            instance.points += ProfileCompletionPoints.objects.last().value
            instance.profile_completion_point = '1'
            instance.save()
        return Response(serializer.data)


class ReferralAPIView(generics.GenericAPIView):
    serializer_class = ReferralSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        if user.referral is not None: raise ValidationError(
            {'user': _('کاربر گرامی شما قبلا معرف خود را ثبت کرده اید.')})
        ref_user = User.objects.get(phone_number=data['phone_number'])
        user.points += 10
        user.referral = ref_user
        user.save()

        ref_user.user_referrals.add(user)
        ref_user.points += 10
        ref_user.save()
        return Response(status=HTTP_200_OK)


class GetRolesAPIView(generics.ListAPIView):
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    queryset = Role.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def five_minute_activity_point(request):
    if request.method == 'POST':
        user = request.user
        user.points += ActivityPoint.objects.last().value
        user.save()
        return Response({'isDone': True}, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def app_has_update(request):
    if request.method == 'GET':
        obj = AppUpdate.objects.last()
        return Response({'isDone': True, "data": {"has_update": obj.value}}, status=HTTP_200_OK)
