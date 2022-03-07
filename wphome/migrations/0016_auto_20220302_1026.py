# Generated by Django 3.2.8 on 2022-03-02 06:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wphome', '0015_delete_searchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='views', to=settings.AUTH_USER_MODEL, verbose_name='بازدید کنندگان'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک ها'),
        ),
    ]
