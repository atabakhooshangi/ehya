# Generated by Django 3.2.8 on 2021-11-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTicketAnswerLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=3, help_text='مقدار وارد شده تعیین میکند که کاربر حداکثر تا چند پاسخ در بدنه تیکت پشتیبانی خود میتواند مطرح کند.', verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'محدودیت تعداد پاسخ تیکت پشتیبانی',
                'verbose_name_plural': 'محدودیت تعداد پاسخ تیکت پشتیبانی ',
            },
        ),
    ]
