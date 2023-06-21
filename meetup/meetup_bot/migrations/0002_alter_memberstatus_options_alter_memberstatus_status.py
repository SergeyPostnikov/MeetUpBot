# Generated by Django 4.2 on 2023-06-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memberstatus',
            options={'verbose_name': 'статус участника', 'verbose_name_plural': 'статусы участника'},
        ),
        migrations.AlterField(
            model_name='memberstatus',
            name='status',
            field=models.CharField(choices=[('1', 'Посетитель'), ('2', 'Докладчик'), ('3', 'Организатор')], db_index=True, default='1', max_length=1, verbose_name='Статус участника'),
        ),
    ]
