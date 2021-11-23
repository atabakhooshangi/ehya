# Internal imports
from ticket.permissions import IsTreasureAdminOrSeniorAdmin
from .models import Treasury
from .serializers import TreasureSerializer
from accounts.renderers import Renderer, SimpleRenderer

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
        objs = Treasury.objects.filter(user=request.user)
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class GetAllTreasuresAPIView(generics.ListAPIView):
    serializer_class = TreasureSerializer
    permission_classes = [IsTreasureAdminOrSeniorAdmin]
    renderer_classes = [Renderer]
    queryset = Treasury.objects.all()


class RetrieveTreasuresAPIView(generics.RetrieveAPIView):
    serializer_class = TreasureSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [Renderer]

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(Treasury, id=self.kwargs['pk'])
        serializer = self.serializer_class(obj)
        if self.request.user.role in ['مدیر کل', 'مدیر گنجینه'] or self.request.user == obj.user:
            return Response(serializer.data, HTTP_200_OK)
        return Response({'user': 'کاربر مجاز به انجام این عملیات نمیباشد'}, status=HTTP_403_FORBIDDEN)
