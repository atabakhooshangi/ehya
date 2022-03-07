# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import json
# import requests
# from .models import SendSMS
# from .tasks import send_sms_task
#
#
# @receiver(post_save, sender=SendSMS)
# def send_mass_sms(sender, instance, created, *args, **kwargs):
#     if instance.topic:
#         send_sms_task.delay(instance.id)
