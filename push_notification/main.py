from django.db.models import QuerySet
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from .models import PushNotificationSections
from accounts.models import User
import threading


class PushNotification:
    def __init__(self, title: str, body: str, push_type: str, user: QuerySet = None, image=None, section: str = None):
        self.section = section
        self.title = title
        self.body = body
        self.push_type = push_type
        self.user = user
        self.image = image

    def check_section(self):
        if getattr(PushNotificationSections.objects.last(), self.section) is True:
            return True
        if self.section == 'push':
            return True
        return False

    def find_devices(self):
        devices = FCMDevice.objects.filter(user__in=self.user)
        return devices

    def send(self):
        if self.check_section():
            if self.push_type == 'all':
                FCMDevice.objects.send_message(message=Message(
                    notification=Notification(
                        title=self.title, body=self.body, image=self.image
                    )
                )
                )
            if self.push_type in ['personal', 'group']:
                devices = self.find_devices()
                devices.send_message(message=Message(
                    notification=Notification(
                        title=self.title, body=self.body, image=self.image
                    )
                )
                )
        return "Done"


class PushThread(threading.Thread):
    def __init__(self, section: str, title: str, body: str, push_type: str, user: QuerySet = None, image=None):
        self.section = section
        self.title = title
        self.body = body
        self.push_type = push_type
        self.user = user
        self.image = image
        threading.Thread.__init__(self)

    def run(self):
        notif_instance = PushNotification(section=self.section, title=self.title, body=self.body,
                                          push_type=self.push_type, user=self.user, image=self.image)
        notif_instance.send()
