# from django.utils.translation import ugettext as _
# from rest_framework import serializers
# from jalali_date import datetime2jalali
# from rest_framework.generics import get_object_or_404
# from .models import WpPosts, WpComments
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     comment_date = serializers.SerializerMethodField()
#     comment_date_gmt = serializers.SerializerMethodField()
#
#     class Meta:
#         model = WpComments
#         fields = [
#             'id',
#             'comment_post_id',
#             'comment_author',
#             'comment_author_email',
#             'comment_author_url',
#             'comment_author_ip',
#             'comment_date',
#             'comment_date_gmt',
#             'comment_content',
#             'comment_karma',
#             'comment_approved',
#             'comment_agent',
#             'comment_type',
#             'comment_parent',
#             'user_id',
#         ]
#
#     def get_comment_date(self, obj):
#         return datetime2jalali(obj.comment_date).strftime('%y/%m/%d _ %H:%M:%S') if obj.comment_date else None
#
#     def get_comment_date_gmt(self, obj):
#         return datetime2jalali(obj.comment_date_gmt).strftime('%y/%m/%d _ %H:%M:%S') if obj.comment_date_gmt else None
#
#
# class PostSerializer(serializers.ModelSerializer):
#     post_date = serializers.SerializerMethodField()
#     post_date_gmt = serializers.SerializerMethodField()
#     post_modified = serializers.SerializerMethodField()
#     post_modified_gmt = serializers.SerializerMethodField()
#     comments = serializers.SerializerMethodField()
#
#     class Meta:
#         model = WpPosts
#         fields = [
#             'id',
#             'post_author',
#             'post_date',
#             'post_date_gmt',
#             'post_content',
#             'post_title',
#             'post_excerpt',
#             'post_status',
#             'comment_status',
#             'ping_status',
#             'post_password',
#             'post_name',
#             'to_ping',
#             'pinged',
#             'guid',
#             'post_modified',
#             'post_modified_gmt',
#             'post_content_filtered',
#             'post_parent',
#             'menu_order',
#             'post_type',
#             'post_mime_type',
#             'comment_count',
#             'comments'
#
#         ]
#
#     def get_post_date(self, obj):
#         return datetime2jalali(obj.post_date).strftime('%y/%m/%d _ %H:%M:%S') if obj.post_date else None
#
#     def get_post_date_gmt(self, obj):
#         return datetime2jalali(obj.post_date_gmt).strftime('%y/%m/%d _ %H:%M:%S') if obj.post_date_gmt else None
#
#     def get_post_modified(self, obj):
#         return datetime2jalali(obj.post_modified).strftime('%y/%m/%d _ %H:%M:%S') if obj.post_modified else None
#
#     def get_post_modified_gmt(self, obj):
#         return datetime2jalali(obj.post_modified_gmt).strftime('%y/%m/%d _ %H:%M:%S') if obj.post_modified_gmt else None
#
#     def get_comments(self, obj):
#         comments = WpComments.objects.filter(comment_post_id=obj.id)
#         return CommentSerializer(comments, many=True).data
#
#
# class CommentCreteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WpComments
#         fields = [
#             'comment_id',
#             'comment_post_id',
#             'comment_author_email',
#             'comment_author_url',
#             'comment_author_ip',
#             'comment_date',
#             'comment_date_gmt',
#             'comment_content',
#             'comment_karma',
#             'comment_approved',
#             'comment_agent',
#             'comment_type',
#             'comment_parent',
#             'user_id',
#         ]
#
#     def validate(self, attrs):
#         try:
#             WpPosts.objects.get(id=attrs['comment_post_id'])
#         except Exception:
#             raise serializers.ValidationError({'Post': 'Post Object does not exist'})
#
#         return attrs
#
#     def save(self, **kwargs):
#         WpComments.objects.create(comment_author=kwargs['user'], **self.validated_data)
