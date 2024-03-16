import datetime
from celery import shared_task
from .models import Post


@shared_task
def check_posts_to_publish():
    query = Post.objects.filter(status='5', date_to_publish__isnull=False)
    if query.exists():
        posts_to_perform = query.filter(date_to_publish__gte=datetime.datetime.now())
        for post in posts_to_perform:
            post.status = '1'
            post.date_to_publish = datetime.datetime.now()
            post.save()

        return
    return "No post to publish"
