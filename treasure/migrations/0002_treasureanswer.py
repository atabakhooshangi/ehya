# Generated by Django 3.2.8 on 2021-11-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasure', '0001_initial'),
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
    ]
