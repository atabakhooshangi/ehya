from datetime import datetime, date, time, timezone, timedelta
from django.core.management.base import BaseCommand, CommandError
from accounts.models import Role, ProfileCompletionPoints
from support.models import SupportSection, SupportTicketAnswerLimit
from ticket.models import Section, TicketAnswerLimit, TicketPointCost
from django.contrib.auth.views import get_user_model

User = get_user_model()

Role_list = ['عضو عادی', 'عضو فعال', 'کارشناس', 'کارشناس ارشد', 'مدیر', 'مدیر ارشد', 'دانشجو', 'استاد', 'حکیم',
             'عضو جامعه', 'شورای مرکزی', 'مدیر کل', 'مدیر مطب', 'مدیر ارشد مطب', 'مدیر سایت', 'مدیر ارشد سایت',
             'مدیر اپلیکیشن', 'مدیر ارشد اپلیکیشن', 'مدیر روابط عمومی', 'مدیر ارشد روابط عمومی', 'مدیر آموزش',
             'مدیر ارشد آموزش']

Support_Sections_List = ['اپلیکیشن', 'مطب', 'سایت', 'آموزش', 'عمومی']


class Command(BaseCommand):
    help = 'ساخت نقش های کاربری'

    def handle(self, *args, **options):
        for i in Role_list:
            Role.objects.create(name=i, is_expert=True if 'ارشد' in i else False)
        for k in Support_Sections_List:
            SupportSection.objects.create(name=k)

        ProfileCompletionPoints.objects.create(value=10)
        SupportTicketAnswerLimit.objects.create(value=3)
        TicketAnswerLimit.objects.create(value=3)
        TicketPointCost.objects.create(value=5)

        admin_user = User.objects.create_superuser(phone_number='09121111111', password='1')
        admin_user.role = Role.objects.get(name='مدیر کل')
        admin_user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully Created Roles'))
