# Internal imports
from ticket.permissions import IsTreasureAdminOrSeniorAdmin
from .models import Treasury, TreasureAnswer
from .serializers import TreasureSerializer, GetTreasureSerializer, TreasureAnswerSerializer
from accounts.renderers import Renderer
from accounts.models import User

# Django imports
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Rest Framework imports
from rest_framework.decorators import api_view, permission_classes, authentication_classes, renderer_classes
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


def treasure_permission_checker(user: User) -> bool:
    if user.is_superuser:
        return True
    for role in user.role.all():
        if 'treasure.view_treasury' in role.get_role_permissions:
            return True


class CreateTreasureAPIView(generics.GenericAPIView):
    serializer_class = TreasureSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if treasure_permission_checker(user=request.user):
            objs = Treasury.objects.all()
        else:
            objs = Treasury.objects.filter(user=request.user)
        serializer = GetTreasureSerializer(objs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class GetAllTreasuresAPIView(generics.ListAPIView):
    serializer_class = GetTreasureSerializer
    permission_classes = [IsTreasureAdminOrSeniorAdmin]
    renderer_classes = [Renderer]
    queryset = Treasury.objects.all()


def ret_permission_checker(user: User, role_list: list) -> bool:
    if user.is_superuser:
        return True
    for role in user.role.all():
        if role.name in role_list:
            return True


class RetrieveTreasuresAPIView(generics.GenericAPIView):
    serializer_class = GetTreasureSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Treasury, id=int(self.request.META['HTTP_ID']))
        serializer = self.serializer_class(obj)
        if ret_permission_checker(user=request.user,
                                  role_list=['مدیر کل', 'مدیر گنجینه']) or self.request.user == obj.user:
            return Response(serializer.data, HTTP_200_OK)
        return Response({'user': 'کاربر مجاز به انجام این عملیات نمیباشد'}, status=HTTP_403_FORBIDDEN)
