# Generated by Django 3.2.8 on 2021-11-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0009_alter_ticket_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketAnswerLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=3, help_text='مقدار وارد شده تعیین میکند که کاربر حداکثر تا چند پاسخ در بدنه پرسش خود میتواند مطرح کند.', verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'محدودیت تعداد پاسخ',
                'verbose_name_plural': 'محدودیت تعداد پاسخ',
            },
        ),
    ]
