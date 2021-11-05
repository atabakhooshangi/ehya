# Generated by Django 3.2.8 on 2021-11-04 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_alter_ticket_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام بخش')),
            ],
            options={
                'verbose_name': 'بخش سلامت',
                'verbose_name_plural': 'بخش های سلامت',
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='ticket',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticket.section', verbose_name='بخش مربوطه'),
        ),
    ]
