# Generated by Django 4.2 on 2023-06-22 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_bot', '0004_feedback_is_answered_alter_member_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='end_time',
            field=models.TimeField(null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='report',
            name='start_time',
            field=models.TimeField(null=True, verbose_name='Дата начала'),
        ),
    ]