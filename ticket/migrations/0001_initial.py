# Generated by Django 3.2.8 on 2021-10-19 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ticket.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=255, verbose_name='عنوان')),
                ('section', models.CharField(blank=True, max_length=50, verbose_name='بخش')),
                ('request_text', models.TextField(blank=True, verbose_name='متن درخواست')),
                ('file', models.FileField(blank=True, null=True, upload_to=ticket.models.upload_location, verbose_name='فایل الصاقی')),
                ('status', models.CharField(choices=[('1', 'دیده نشده'), ('2', 'پاسخ داده شده'), ('3', 'بسته شده')], default=1, max_length=1, verbose_name='وضعیت')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت ها',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='متن پاسخ')),
                ('seen', models.BooleanField(default=False, verbose_name='دیده شده')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket', verbose_name='تیکت مربوطه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ',
                'verbose_name_plural': 'پاسخ ها',
                'ordering': ('created_at',),
            },
        ),
    ]
