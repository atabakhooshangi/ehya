# Generated by Django 3.2.8 on 2022-02-03 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wphome', '0010_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='s', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان'),
        ),
    ]
