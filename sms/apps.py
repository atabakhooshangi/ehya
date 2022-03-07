from django.apps import AppConfig


class SmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms'
    verbose_name = "پیامک ها"

    # def ready(self):
    #     import sms.signals
