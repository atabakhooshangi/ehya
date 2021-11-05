from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehyasalamat.settings')

app = Celery('exchange')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # '10m': {
    #     'task': 'datafeed.tasks.create_10m_datafeed',
    #     'schedule': 3,
    # },

}

app.autodiscover_tasks()
