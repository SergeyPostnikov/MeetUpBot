from django.db import models
from django.core.validators import MinValueValidator


class Meetup(models.Model):
    theme = models.CharField(
        'Тема',
        max_length=150,
    )
    description = models.TextField(
        'Описание',
        max_length=500,
    )
    date = models.DateField(
        'Дата',
    )

    class Meta:
        verbose_name = 'митап'
        verbose_name_plural = 'митапы'

    def __str__(self):
        return f'{self.theme}({self.date})'


class Member(models.Model):
    meetup = models.ManyToManyField(
        Meetup,
        through='MemberStatus',
        verbose_name='митап',
    )
    name = models.CharField(
        'Имя',
        max_length=50,
    )
    tg_name = models.CharField(
        'Никнейм',
        max_length=50,
    )
    tg_id = models.BigIntegerField(
        'ID пользователя телегам',
    )
    about = models.TextField(
        'О себе',
        max_length=500,
    )

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'

    def __str__(self):
        return f'{self.name}({self.tg_name})'


class MemberStatus(models.Model):
    USER = '1'
    SPEAKER = '2'
    ADMIN = '3'
    MEMBER_STATUS = (
        ('1', 'Посетитель'),
        ('2', 'Докладчик'),
        ('3', 'Организатор'),
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name='участник',
    )
    meetup = models.ForeignKey(
        Meetup,
        on_delete=models.CASCADE,
        verbose_name='Митап',
    )
    status = models.CharField(
        'Статус участника',
        max_length=1,
        choices=MEMBER_STATUS,
        db_index=True,
        default=USER,
    )
    donate_sum = models.DecimalField(
        'Сумма пожертвования',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
    )


    class Meta:
        verbose_name = 'статус участника'
        verbose_name_plural = 'статусы участника'


class Report(models.Model):
    speaker = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Докладчик',
    )
    meetup = models.ForeignKey(
        Meetup,
        on_delete=models.CASCADE,
        verbose_name='Митап',
    )
    theme = models.CharField(
        'Тема',
        max_length=150,
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_finished = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'доклад'
        verbose_name_plural = 'доклады'

    def __str__(self):
        return f'{self.theme}({self.speaker})'


class Feedback(models.Model):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    GRADES = (
        ('1', 'Не стоит внимания'),
        ('2', 'Так себе'),
        ('3', 'Сойдёт'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name='Участник',
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        verbose_name='Доклад',
    )
    text = models.TextField(
        'Отклик',
        max_length=500,
    )
    is_question = models.BooleanField(
        'Это вопрос',
        default=False,
        db_index=True,
    )
    grade = models.CharField(
        'Оценка',
        max_length=1,
        choices=GRADES,
    )

    class Meta:
        verbose_name = 'отклик'
        verbose_name_plural = 'отклики'

    def __str__(self):
        return f'{self.report}({self.member})'
