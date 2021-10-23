import json
from django.utils.translation import ugettext as _
from .serializers import RegisterLoginSerializer, VerificationCodeSerializer, UserSerializer, ReferralSerializer
import requests
from random import randint
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from .utils import get_visitor_ipaddress

User = get_user_model()


class RegisterLoginAPIView(generics.GenericAPIView):
    serializer_class = RegisterLoginSerializer
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
        user.save()
        message = f'   کد احراز هویت شما : {code}'
        url = 'http://185.4.28.100/class/sms/restful/sendSms_OneToMany.php'

        params = {'uname': 'hakimdr', 'pass': '52b@4ED', 'from': '+985000171', 'to': [user.phone_number],
                  'msg': f'{message}'}

        response = requests.post(url, data=json.dumps(params))
        return Response('کاربر با موفقیت ساخته شد', status=HTTP_201_CREATED)


class VerifyAuthenticationCodeAPIView(generics.GenericAPIView):
    serializer_class = VerificationCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=HTTP_200_OK)


class UserProfileAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReferralAPIView(generics.GenericAPIView):
    serializer_class = ReferralSerializer
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
        return Response('با موفقیت ثبت شد.', status=HTTP_200_OK)
