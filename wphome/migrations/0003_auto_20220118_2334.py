# Generated by Django 3.2.8 on 2022-01-18 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wphome', '0002_auto_20211228_2330'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WpComments',
        ),
        migrations.DeleteModel(
            name='WpPosts',
        ),
    ]
