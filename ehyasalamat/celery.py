from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehyasalamat.settings')

app = Celery('ehyasalamat')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'to_publish': {
        'task': 'wphome.tasks.check_posts_to_publish',
        'schedule': 300,
    },

}

app.autodiscover_tasks()
