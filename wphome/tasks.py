import datetime
from celery import shared_task
from django.conf import settings

from push_notification.main import PushThread
from .models import Post, upload_thumbnail_location


@shared_task
def check_posts_to_publish():
    query = Post.objects.filter(status='5', date_to_publish__isnull=False)
    if query.exists():
        posts_to_perform = query.filter(date_to_publish__lte=datetime.datetime.now())
        for post in posts_to_perform:
            post.status = '1'
            post.date_to_publish = datetime.datetime.now()
            if post.send_push:
                photo_url = upload_thumbnail_location(post, str(post.push_notif_thumbnail))
                url = 'http://' + '87.107.172.122' + settings.MEDIA_URL + photo_url
                PushThread(section='home', title=post.title, body=post.push_notif_description,
                           push_type='all',
                           image=str(url)).start()
            post.save()

        return
    return "No post to publish"
