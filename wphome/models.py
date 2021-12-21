from django.db import models


class WpPosts(models.Model):
    post_author = models.PositiveBigIntegerField(null=True, blank=True)
    post_date = models.DateTimeField(null=True, blank=True)
    post_date_gmt = models.DateTimeField(null=True, blank=True)
    post_content = models.TextField(null=True, blank=True)
    post_title = models.TextField(null=True, blank=True)
    post_excerpt = models.TextField(null=True, blank=True)
    post_status = models.CharField(max_length=20, null=True, blank=True)
    comment_status = models.CharField(max_length=20, null=True, blank=True)
    ping_status = models.CharField(max_length=20, null=True, blank=True)
    post_password = models.CharField(max_length=255, null=True, blank=True)
    post_name = models.CharField(max_length=200, null=True, blank=True)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField(null=True, blank=True)
    post_modified_gmt = models.DateTimeField(null=True, blank=True)
    post_content_filtered = models.TextField(null=True, blank=True)
    post_parent = models.PositiveBigIntegerField(null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)
    menu_order = models.IntegerField(null=True, blank=True)
    post_type = models.CharField(max_length=20, null=True, blank=True)
    post_mime_type = models.CharField(max_length=100, null=True, blank=True)
    comment_count = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Wp Post'
        verbose_name_plural = 'Wp Posts'
        ordering = ('post_date',)


class WpComments(models.Model):
    comment_post_id = models.PositiveBigIntegerField(null=True, blank=True)
    comment_author = models.TextField(null=True)
    comment_author_email = models.CharField(max_length=100, null=True)
    comment_author_url = models.CharField(max_length=200, null=True)
    comment_author_ip = models.CharField(db_column='comment_author_IP', max_length=100,
                                         null=True)  # Field name made lowercase.
    comment_date = models.DateTimeField(null=True, auto_now_add=True)
    comment_date_gmt = models.DateTimeField(null=True, auto_now=True)
    comment_content = models.TextField(null=True)
    comment_karma = models.IntegerField(null=True)
    comment_approved = models.CharField(max_length=20, null=True)
    comment_agent = models.CharField(max_length=255, null=True)
    comment_type = models.CharField(max_length=20, null=True)
    comment_parent = models.PositiveBigIntegerField(null=True)
    user_id = models.PositiveBigIntegerField(null=True)

    class Meta:
        verbose_name = 'Wp Comment'
        verbose_name_plural = 'Wp Comments'
        ordering = ('comment_date',)
