# Generated by Django 4.2 on 2023-06-22 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_bot', '0003_alter_feedback_grade_alter_feedback_is_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_answered',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Дан ответ'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Профессия'),
        ),
    ]
