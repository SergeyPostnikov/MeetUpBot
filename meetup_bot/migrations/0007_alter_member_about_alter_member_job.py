# Generated by Django 4.2 on 2023-06-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_bot', '0006_member_job_alter_feedback_grade_alter_member_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='about',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='member',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Профессия'),
        ),
    ]