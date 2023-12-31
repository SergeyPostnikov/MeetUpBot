# Generated by Django 4.2 on 2023-06-21 11:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=150, verbose_name='Тема')),
                ('description', models.TextField(max_length=500, verbose_name='Описание')),
                ('date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'митап',
                'verbose_name_plural': 'митапы',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('tg_name', models.CharField(max_length=50, verbose_name='Никнейм')),
                ('tg_id', models.BigIntegerField(verbose_name='ID пользователя телегам')),
                ('about', models.TextField(max_length=500, verbose_name='О себе')),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=150, verbose_name='Тема')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_finished', models.BooleanField(default=False)),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.meetup', verbose_name='Митап')),
                ('speaker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.member', verbose_name='Докладчик')),
            ],
            options={
                'verbose_name': 'доклад',
                'verbose_name_plural': 'доклады',
            },
        ),
        migrations.CreateModel(
            name='MemberStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(1, 'Посетитель'), (2, 'Докладчик'), (3, 'Организатор')], db_index=True, default=1, max_length=1, verbose_name='Статус участника')),
                ('donate_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма пожертвования')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.meetup', verbose_name='Митап')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.member', verbose_name='участник')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='meetup',
            field=models.ManyToManyField(through='meetup_bot.MemberStatus', to='meetup_bot.meetup', verbose_name='митап'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Отклик')),
                ('is_question', models.BooleanField(db_index=True, default=False, verbose_name='Вопрос?')),
                ('grade', models.CharField(choices=[(1, 'Не стоит внимания'), (2, 'Так себе'), (3, 'Сойдёт'), (4, 'Хорошо'), (5, 'Отлично')], max_length=1, verbose_name='Оценка')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.member', verbose_name='Участник')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup_bot.report', verbose_name='Доклад')),
            ],
            options={
                'verbose_name': 'отклик',
                'verbose_name_plural': 'отклики',
            },
        ),
    ]
