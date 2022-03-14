from django.utils.translation import ugettext as _
from rest_framework import serializers
from jalali_date import datetime2jalali

from .models import Post, Tag, Category, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        if value.approved:
            serializer = self.parent.parent.__class__(value, context=self.context)
            return serializer.data
        return "None"


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    user = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'date_created', 'children')

    def get_user(self, obj):
        return obj.user.first_name

    def get_date_created(self, obj):
        return datetime2jalali(obj.date_created).strftime('%y/%m/%d _ %H:%M:%S')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'parent', 'related_post')

    def save(self, **kwargs):
        comment = Comment.objects.create(user=kwargs['user'], text=self.validated_data['text'],
                                         parent=self.validated_data['parent'],
                                         related_post=self.validated_data['related_post'])
        return comment


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')


class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostsRetrieveSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    date_published = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'categories', 'image', 'file', 'share_link', 'liked', 'likes_count', 'views_count',
            'favorite', 'short_description', 'tags', 'link_tv', 'radio_ehya', 'ehya_tv', 'special_post',
            'comments', 'date_published')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_views_count(self, obj):
        return obj.views.count()

    def get_liked(self, obj):
        if self.context.get('user') in obj.likes.all():
            return True
        return False

    def get_categories(self, obj):
        categories = obj.categories.all()
        resp = []
        for category in categories:
            resp.append(category.name)
        return resp

    def get_favorite(self, obj):
        if self.context.get('user') in obj.favorite.all():
            return True
        return False

    def get_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data

    def get_date_published(self, obj):
        return datetime2jalali(obj.date_created).strftime('%y/%m/%d _ %H:%M:%S')

    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.filter(approved=True), many=True).data


class PostsListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    date_published = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'categories', 'image', 'file', 'share_link', 'liked', 'likes_count', 'views_count',
            'favorite', 'short_description', 'tags', 'link_tv', 'radio_ehya', 'ehya_tv', 'special_post',
            'date_published')

    def get_favorite(self, obj):
        if self.context.get('user') in obj.favorite.all():
            return True
        return False

    def get_categories(self, obj):
        categories = obj.categories.all()
        resp = []
        for category in categories:
            resp.append(category.name)
        return resp

    def get_views_count(self, obj):
        return obj.views.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        if self.context.get('user') in obj.likes.all():
            return True
        return False

    def get_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data

    def get_date_published(self, obj):
        return datetime2jalali(obj.date_created).strftime('%y/%m/%d _ %H:%M:%S')
