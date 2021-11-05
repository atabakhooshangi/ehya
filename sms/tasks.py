from celery import shared_task
from .models import SendSMS
from .utils import send_sms


@shared_task
def send_sms_task(instance_id):
    instance = SendSMS.objects.get(id=instance_id)

    if instance.sms_type == '2':
        for user in instance.recipients.all():
            message = instance.text
            if '%name%' in message:
                message = message.replace('%name%', f'{user.first_name} {user.last_name}')
            if '%points%' in message:
                message = message.replace('%points%', user.points)
            send_sms(message=message, recipients=[user.phone_number])

    if instance.sms_type == '1':
        send_sms(message=instance.text, recipients=list(instance.recipients.values_list('phone_number', flat=True)))
    return "Done"
