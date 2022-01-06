# Internal imports
import json

import requests
from rest_framework.decorators import api_view, permission_classes

from .models import WpPosts, WpComments
# from .serializers import PostSerializer, CommentCreteSerializer

from accounts.renderers import Renderer, SimpleRenderer
# Rest Framework imports
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


# class PostGetAPIView(generics.ListAPIView):
#     serializer_class = PostSerializer
#     renderer_classes = [Renderer]
#     permission_classes = [AllowAny]
#
#     def get_queryset(self):
#         return WpPosts.objects.all()
#
#
# class RetrievePostAPIView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = PostSerializer
#     renderer_classes = [Renderer]
#
#     def get_object(self):
#         return get_object_or_404(WpPosts, id=self.request.META['HTTP_ID'])
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.get_object())
#         return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_api(request):
    if request.method == 'GET':
        page_num = request.META.get('HTTP_PAGE')
        url = 'https://ravazadeh.com/wp-json/wp/v2/posts'
        params = {'page': str(page_num)}
        response = requests.get(url, params=params)
        all_pages = response.headers.get('X-WP-TotalPages')
        all_posts = response.headers.get('X-WP-Total')
        res = json.loads(response.content)
        return Response(res, status=HTTP_200_OK, headers={'total_pages': all_pages, 'total_posts': all_posts})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_post_api(request):
    if request.method == 'GET':
        post_id = request.META.get('HTTP_ID')
        url = f'https://ravazadeh.com/wp-json/wp/v2/posts/{post_id}'
        response = requests.get(url)
        res = json.loads(response.content)
        return Response(res, status=HTTP_200_OK)

# class CreateCommentAPIView(generics.CreateAPIView):
#     serializer_class = CommentCreteSerializer
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [SimpleRenderer]
#
#     def perform_create(self, serializer):
#         serializer = self.serializer_class(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=self.request.user)
