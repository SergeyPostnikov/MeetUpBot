# Generated by Django 4.2 on 2023-06-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_bot', '0005_alter_report_end_time_alter_report_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='job',
            field=models.CharField(blank=True, max_length=100, verbose_name='Профессия'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='grade',
            field=models.CharField(blank=True, choices=[('1', 'Не стоит внимания'), ('2', 'Так себе'), ('3', 'Сойдёт'), ('4', 'Хорошо'), ('5', 'Отлично')], max_length=1, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
    ]
