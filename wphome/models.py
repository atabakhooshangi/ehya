from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from django.db.models import Q

User = get_user_model()


class PostManager(models.Manager):
    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(category__name__icontains=query)
        )
        return self.get_queryset().filter(lookup, published=True).distinct()


def upload_audo_file_location(instance, filename):
    extension = filename.split('.')[-1]
    if len(Post.objects.all()) > 0:
        post_id = Post.objects.last().id + 1
    else:
        post_id = 1
    return f'uploads/radio_ehya/Post_radi_ehya_{post_id}.{extension}'


def upload_image_location(instance, filename):
    extension = filename.split('.')[-1]
    if len(Post.objects.all()) > 0:
        post_id = Post.objects.last().id + 1
    else:
        post_id = 1
    return f'uploads/post_images/Post_image_{post_id}.{extension}'


class CategoryManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class Category(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('نام'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    objects = CategoryManager()

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name=_('برچسب'))

    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب ها')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('عنوان'))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=False, blank=False,
                                 verbose_name=_('دسته بندی'))
    image = models.ImageField(upload_to=upload_image_location, verbose_name=_('تصویر پست'), null=True, blank=True)
    file = models.FileField(upload_to=upload_audo_file_location, verbose_name=_('فایل صوتی'), null=True, blank=True)
    short_description = models.TextField(verbose_name=_('خلاصه مطلب'))
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name=_('برچسب ها'))
    link_tv = models.URLField(verbose_name=_('لینک احیا تی وی'),
                              help_text=_('اگر پست از نوع احیا تی وی بود لینک آن اینجا درج شود.'), null=True,
                              blank=True)
    radio_ehya = models.BooleanField(default=False, verbose_name=_('رادیو احیا'))
    ehya_tv = models.BooleanField(default=False, verbose_name=_('احیا تی وی'))
    published = models.BooleanField(default=True, verbose_name=_('منتشر شده'))
    date_published = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))

    objects = PostManager()

    class Meta:
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')
        ordering = ('date_published',)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('کاربر'))
    related_post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name=_('پست مرتبط'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    text = models.TextField(verbose_name=_('متن'))
    approved = models.BooleanField(default=False, verbose_name=_('تایید شده'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنت ها')

    class MPTTMeta:
        order_insertion_by = ['date_created']

    def __str__(self):
        return f"{self.user}'s comment for post {self.related_post.id}"


class CommentPoint(models.Model):
    value = models.PositiveIntegerField(default=5, verbose_name=_('مقدار'))

    class Meta:
        verbose_name = _('امتیاز ثبت کامنت')
        verbose_name_plural = _('امتیاز ثبت کامنت')

    def __str__(self):
        return str(self.value)
