# Generated by Django 3.2.8 on 2022-02-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wphome', '0008_auto_20220203_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='push_notif_description',
            field=models.TextField(default='s', verbose_name='توضیح مختصر پوش نوتیفیکیشن'),
            preserve_default=False,
        ),
    ]
