from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _
from django.contrib.auth.views import get_user_model
from django.db.models import Q

User = get_user_model()

POST_STATUS = (
    ('1', 'منتشر شده'),
    ('2', 'عدم انتشار'),
    ('3', 'برای بازبینی'),
    ('4', 'پیش نویس'),
    ('5', 'در صف انتشار')
)


class PostManager(models.Manager):
    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(category__name__icontains=query)
        )
        return self.get_queryset().filter(lookup, status='1').distinct()


def upload_audo_file_location(instance, filename):
    # extension = filename.split('.')[-1]
    return f'uploads/radio_ehya/{filename}'


def upload_image_location(instance, filename):
    # extension = filename.split('.')[-1]
    # slug = instance.slug.replace('_', '-')
    # return f'uploads/post_images/Post_image_{instance.title}.{extension}'
    return f'uploads/post_images/{filename}'


def upload_thumbnail_location(instance, filename):
    # extension = filename.split('.')[-1]
    # return f'uploads/push_notif_thumbnails/Post_thumbnail_{instance.title}.{extension}'
    return f'uploads/push_notif_thumbnails/{filename}'


def upload_icon_location(instance, filename):
    # extension = filename.split('.')[-1]
    # return f'uploads/push_notif_thumbnails/Post_thumbnail_{instance.title}.{extension}'
    return f'uploads/category_icons/{filename}'


class CategoryManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class Category(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('نام'))
    icon = models.ImageField(upload_to=upload_icon_location, verbose_name=_('آیکون'), null=True, blank=True)
    code_1 = models.CharField(_('کد رنگ 1'), max_length=20, null=True, blank=True)
    code_2 = models.CharField(_('کد رنگ 2'), max_length=20, null=True, blank=True)
    text_color = models.CharField(_('کد رنگ متن'), max_length=20, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name=_('والد'))

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
    categories = models.ManyToManyField(to=Category, blank=False, verbose_name=_('دسته بندی'))
    image = models.ImageField(upload_to=upload_image_location, verbose_name=_('تصویر پست'), null=True, blank=True)
    file = models.FileField(upload_to=upload_audo_file_location, verbose_name=_('فایل صوتی'), null=True, blank=True)
    short_description = models.TextField(verbose_name=_('خلاصه مطلب'))
    description = models.TextField(verbose_name=_('متن کامل مطلب'), null=True)
    likes = models.ManyToManyField(to=User, blank=True, verbose_name=_('لایک ها'), related_name='likes')
    share_link = models.CharField(_('لینک اشتراک گذاری'), max_length=250, null=True, blank=True)
    push_notif_description = models.TextField(verbose_name=_('توضیح مختصر پوش نوتیفیکیشن'))
    push_notif_thumbnail = models.ImageField(upload_to=upload_thumbnail_location,
                                             verbose_name=_('تصویر پوش نوتیفیکیشن'),
                                             null=True, blank=True)
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name=_('برچسب ها'))
    views = models.ManyToManyField(to=User, blank=True, verbose_name=_('بازدید کنندگان'), related_name='views')
    favorite = models.ManyToManyField(to=User, blank=True, verbose_name=_('غلاقه مندی'), related_name='favorite')
    link_tv = models.URLField(verbose_name=_('لینک احیا تی وی'),
                              help_text=_('اگر پست از نوع احیا تی وی بود لینک آن اینجا درج شود.'), null=True,
                              blank=True)
    radio_ehya = models.BooleanField(default=False, verbose_name=_('رادیو احیا'))
    ehya_tv = models.BooleanField(default=False, verbose_name=_('احیا تی وی'))
    special_post = models.BooleanField(default=False, verbose_name=_('پست ویژه'))
    send_push = models.BooleanField(default=True, verbose_name=_('ارسال پوش نوتیفیکیشن'))
    status = models.CharField(_('وضعیت'), max_length=1, null=True, blank=False, choices=POST_STATUS)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    date_to_publish = models.DateTimeField(null=True, blank=True, verbose_name=_('تاریخ انتشار'))

    objects = PostManager()

    class Meta:
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')
        ordering = ('date_created',)

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="280" height="200" />'.format(self.image.url))
        return "موردی یافت نشد"


@receiver(pre_save, sender=Post)
def delete_old_file(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
            old_thumbnail = sender.objects.get(pk=instance.pk).push_notif_thumbnail
            old_radio = sender.objects.get(pk=instance.pk).file
        except sender.DoesNotExist:
            return

        else:
            img = instance.image
            thumbnail = instance.push_notif_thumbnail
            radio = instance.file
            if not old_image == img:
                old_image.delete(save=False)
            if not old_thumbnail == thumbnail:
                old_thumbnail.delete(save=False)
            if not old_radio == radio:
                old_radio.delete(save=False)


@receiver(pre_delete, sender=Post)
def delete_instance_file(sender, instance, **kwargs):
    instance.image.delete(save=False)
    instance.push_notif_thumbnail.delete(save=False)


class Comment(MPTTModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('کاربر'))
    related_post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name=_('پست مرتبط'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name=_('کامنت والد'))
    text = models.TextField(verbose_name=_('متن'))
    approved = models.BooleanField(default=False, verbose_name=_('تایید شده'))
    point_gained = models.BooleanField(default=False, verbose_name=_('امتیاز کسب شده'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنت ها')

    class MPTTMeta:
        order_insertion_by = ['date_created']

    def __str__(self):
        return f" کامنت {self.user}  برای پست {self.related_post.title}"

# class CommentPoint(models.Model):
#     value = models.PositiveIntegerField(default=5, verbose_name=_('مقدار'))
#
#     class Meta:
#         verbose_name = _('امتیاز ثبت کامنت')
#         verbose_name_plural = _('امتیاز ثبت کامنت')
#
#     def __str__(self):
#         return str(self.value)
