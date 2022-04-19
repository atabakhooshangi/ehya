# Internal imports
import json

from rest_framework.pagination import PageNumberPagination
from mptt.utils import tree_item_iterator
from rest_framework.views import APIView

from ticket.permissions import IsOwner
from rest_framework.decorators import api_view, permission_classes , renderer_classes

from .permissions import post_permission_checker
from .serializers import CategorySerializer, SingleCategorySerializer, PostsListSerializer, CommentCreateSerializer, \
    TagSerializer, PostsRetrieveSerializer
from .models import Category, Post, Comment, Tag
from accounts.renderers import Renderer, SimpleRenderer
# Rest Framework imports
from rest_framework import generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_204_NO_CONTENT , HTTP_404_NOT_FOUND
from rest_framework.response import Response


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(CategoryListAPIView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        checker = post_permission_checker(self.request.user, ['مادران قابله'])
        categories = Category.objects.viewable() if checker else Category.objects.viewable().exclude(name__icontains='مادران')
        return categories


class CategoryTreeRetrieveAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(CategoryTreeRetrieveAPIView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        checker = post_permission_checker(self.request.user, ['مادران قابله'])
        categories = Category.objects.viewable().filter(id=self.kwargs['pk'])
        categories = categories if checker else categories.exclude(name__icontains='مادران')
        return categories


class CategoryRetrieveAPIView(generics.ListAPIView):
    serializer_class = SingleCategorySerializer
    renderer_classes = [Renderer]
    permission_classes = [AllowAny]
    queryset = Category.objects.all()

    def get_queryset(self):
        checker = post_permission_checker(self.request.user, ['مادران قابله'])
        categories = Category.objects.filter(id=self.kwargs['pk'])
        categories = categories if checker else categories.exclude(name__icontains='مادران')
        return categories


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
        checker = post_permission_checker(self.request.user, ['مادران قابله'])
        posts = Post.objects.all() if checker else Post.objects.all().exclude(categories__name__icontains='مادران')
        if param == 'all':
            return posts.filter(status='1')
        if param == 'liked':
            return posts.filter(likes__in=[self.request.user], status='1')
        if param == 'favorite':
            return posts.filter(favorite__in=[self.request.user])
        if param == 'special':
            return posts.filter(special_post=True)
        if param == 'tv':
            return posts.filter(ehya_tv=True)
        if param == 'radio':
            return posts.filter(radio_ehya=True)
        return posts.filter(categories__in=[self.kwargs['id']], status='1')


class PostsSearchView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        param = self.request.query_params.get('q')
        search_q = Post.objects.search(param)
        user = self.request.user
        if post_permission_checker(user, ['مادران قابله']):
            return search_q
        return search_q.exclude(categories__name__icontains='مادران')


class PostRetrieveAPIView(generics.GenericAPIView):
    serializer_class = PostsRetrieveSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super(PostRetrieveAPIView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def get(self,request,*args,**kwargs):
        checker = post_permission_checker(self.request.user, ['مادران قابله'])
        post = get_object_or_404(Post, id=self.kwargs['pk'], status='1')
        if checker:
            return Response(self.serializer_class(post).data,status=HTTP_200_OK)

        post = Post.objects.filter(id=self.kwargs['pk'], status='1').exclude(categories__name__icontains='مادران')
        if post.exists():
            return Response(self.serializer_class(post.first()).data,status=HTTP_200_OK)
        return Response([],status=HTTP_200_OK)



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
    queryset = Comment.objects.all()

    def get_object(self):
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
            result = False
            post.likes.remove(request.user)
        else:
            result = True
            post.likes.add(request.user)

        return Response({'isDone': True, 'data': {'liked': result}}, status=HTTP_200_OK)


class AddOrRemovePostToFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)

        if post.favorite.filter(id=request.user.id).exists():
            result = False
            post.favorite.remove(request.user)
        else:
            result = True
            post.favorite.add(request.user)

        return Response({'isDone': True, 'data': {'favorite': result}}, status=HTTP_200_OK)


class AddPostToViewsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)

        if not post.views.filter(id=request.user.id).exists():
            post.views.add(request.user)

        return Response({'isDone': True}, status=HTTP_200_OK)


class UserFavoritePostsAPIView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    renderer_classes = [Renderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(favorite__in=[self.request.user])


# class GetUserSearchHistory(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated, ]
#     renderer_classes = [Renderer]
#     serializer_class = PostsListSerializer
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         posts = user.searchhistory.posts.all()
#         serializer = self.serializer_class(posts, many=True)
#         return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([Renderer])
@permission_classes([IsAdminUser])
def special_post_indicator(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        post.special_post = False if post.special_post else True
        post.save()
        data = PostsListSerializer(post).data
        return Response(data, status=HTTP_200_OK)
