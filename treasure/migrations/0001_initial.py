# Generated by Django 3.2.8 on 2022-03-07 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import treasure.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TreasureAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام تشکر')),
            ],
            options={
                'verbose_name': 'متن پیام تشکر گنجینه',
                'verbose_name_plural': 'متن پیام تشکر گنجینه',
            },
        ),
        migrations.CreateModel(
            name='Treasury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=225, verbose_name='موضوع')),
                ('link', models.URLField(blank=True, verbose_name='لینک مطلب')),
                ('file', models.FileField(blank=True, null=True, upload_to=treasure.models.upload_location, validators=[treasure.models.file_size], verbose_name='فایل ارسالی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'گنجینه',
                'verbose_name_plural': 'گنجینه ها',
                'ordering': ('created_at',),
            },
        ),
    ]
