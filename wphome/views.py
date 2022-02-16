# Internal imports
import json

from rest_framework.pagination import PageNumberPagination
from mptt.utils import tree_item_iterator
from rest_framework.views import APIView

from ticket.permissions import IsOwner
from rest_framework.decorators import api_view, permission_classes

from .serializers import CategorySerializer, SingleCategorySerializer, PostsListSerializer, CommentCreateSerializer, \
    TagSerializer, PostsRetrieveSerializer
from .models import Category, Post, Comment, Tag
from accounts.renderers import Renderer, SimpleRenderer
# Rest Framework imports
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_204_NO_CONTENT
from rest_framework.response import Response


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.viewable()


class CategoryTreeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        categories = Category.objects.viewable()
        filtered_categories = categories.filter(id=self.kwargs['pk'])
        return filtered_categories


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SingleCategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        categories = Category.objects.viewable()
        filtered_categories = categories.filter(id=self.kwargs['pk'])
        return filtered_categories


class PostsListView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(PostsListView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        param = self.kwargs['id']
        if param == 'all':
            return Post.objects.filter(published=True)
        if param == 'liked':
            return Post.objects.filter(likes__in=[self.request.user], published=True)
        return Post.objects.filter(category_id=self.kwargs['id'], published=True)


class PostsSearchView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        param = self.request.query_params.get('q')
        return Post.objects.search(param)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PostsRetrieveSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(PostRetrieveAPIView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get_object(self):
        print(self.kwargs['pk'])
        return get_object_or_404(Post, id=self.kwargs['pk'], published=True)


class CreateCommentAPIView(generics.GenericAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'isDone': True}, status=HTTP_201_CREATED)


class DeleteCommentAPIView(generics.DestroyAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        print(self.kwargs['pk'])
        return get_object_or_404(Comment, id=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request=self.request, obj=obj)
        self.perform_destroy(obj)
        return Response({'isDone': True}, status=HTTP_204_NO_CONTENT)


class TagListAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()


class AddOrRemovePostToLikesAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return Response({'isDone': True}, status=HTTP_200_OK)


class GetUserSearchHistory(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [Renderer]
    serializer_class = PostsListSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = user.searchhistory.posts.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
