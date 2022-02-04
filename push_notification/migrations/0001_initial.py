# Generated by Django 3.2.8 on 2022-02-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PushNotificationSections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home', models.BooleanField(default=True, verbose_name='خانه')),
                ('inform', models.BooleanField(default=True, verbose_name='اعلانات')),
                ('support', models.BooleanField(default=True, verbose_name='پشتیبانی')),
                ('ticket', models.BooleanField(default=True, verbose_name='پرس و پاسخ')),
                ('treasure', models.BooleanField(default=True, verbose_name='گنجینه')),
            ],
            options={
                'verbose_name': 'بخش های پوش نتیفیکیشن',
                'verbose_name_plural': 'بخش های پوش نتیفیکیشن',
            },
        ),
    ]
