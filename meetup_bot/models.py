from django.db import models
from django.core.validators import MinValueValidator
from datetime import date, time


class MeetupManager(models.Manager):
    def current(self):
        return self.filter(date__gte=date.today()).order_by('date').first()

    def actual(self):
        return self.filter(date__gte=date.today()).order_by('date')

    def users(self):
        return self.current().members.filter(memberstatus__status=MemberStatus.USER)

    def speakers(self):
        return self.current().members.filter(memberstatus__status=MemberStatus.SPEAKER)

    def admins(self):
        return self.current().members.filter(memberstatus__status=MemberStatus.ADMIN)

    def donated_members(self):
        return self.current().members.filter(memberstatus__donate_sum__gte=0)


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
        'Member',
        on_delete=models.CASCADE,
        verbose_name='участник',
    )
    meetup = models.ForeignKey(
        'Meetup',
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

    objects = MeetupManager()

    class Meta:
        verbose_name = 'митап'
        verbose_name_plural = 'митапы'

    def __str__(self):
        return f'{self.theme}({self.date})'

    def register_user(self, tg_id, status=MemberStatus.USER, tg_name='', name=''):
        (member, created) = Member.objects.get_or_create(
                                    tg_id=tg_id,
        )
        save = False

        if not member.name == name and name:
            member.name = name
            save = True
        if not member.tg_name == tg_name and tg_name:
            member.tg_name = tg_name
            save = True
            
        if save:
            member.save()

        (member_status, created) = MemberStatus.objects.get_or_create(
                                    meetup=self,
                                    member=member,
        )
        member.set_status(self, status)
        return member

    def add_report(self, theme, start, end, speaker=None):
        hours, minutes, = start.split(':')

        if int(hours) >= 0 and int(minutes) >= 0:

            start_time = time(hour=int(hours), minute=int(minutes))
        else:
            start_time = time(hour=12, minute=0)

        hours, minutes, = end.split(':')

        if int(hours) >= 0 and int(minutes) >= 0:

            end_time = time(hour=int(hours), minute=int(minutes))
        else:
            end_time = time(hour=12, minute=0)

        (report, created) = Report.objects.get_or_create(
                            meetup=self,
                            theme=theme,
        )
        report.start_time = start_time
        report.end_time = end_time

        if speaker:
            speaker.set_status(self, MemberStatus.SPEAKER)
            report.speaker = speaker
        report.save()

        return report


class Member(models.Model):
    meetup = models.ManyToManyField(
        Meetup,
        through='MemberStatus',
        verbose_name='митап',
        related_name='members',
    )
    name = models.CharField(
        'Имя',

        max_length=100,
    )
    job = models.CharField(
        'Профессия',
        max_length=100,
        blank=True,
        null=True

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
        blank=True,
        null=True
    )
    is_owner = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'

    def __str__(self):
        return f'{self.name}({self.tg_id})'

    def donate(self, current_meetup):
        return MemberStatus.objects.get(meetup=current_meetup, member=self).donate_sum

    def set_status(self, meetup, status):
        (member_status, created) = MemberStatus.objects.get_or_create(meetup=meetup, member=self)
        if not member_status.status == status:
            member_status.status = status
            member_status.save()  # TODO Отправить уведомление о регистрации если надо


    def get_status(self, meetup):
        member_status = MemberStatus.objects.filter(meetup=meetup, member=self)
        if not member_status:
            status = None
        else:
            status = member_status[0].status
        #     member_status.status = MemberStatus.USER
        #     member_status.save()  # TODO Отправить уведомление о регистрации если надо
        return status

    def send_feedback(self, text, report=None, is_question=True):
        if not report:
            report = Report.objects.current_report()
        feedback = Feedback.objects.create(
            member=self,
            report=report,
            text=text,
            is_question=is_question,
        )
        return feedback


class ReportManager(models.Manager):
    def current_report(self):
        return self.filter(
                    is_finished=False,
                    meetup=Meetup.objects.current()
                ).order_by('start_time').first()

    def actual_reports(self):
        return self.filter(
                    is_finished=False,
                    meetup=Meetup.objects.current()
                ).order_by('start_time')

    def current_meetup_reports(self):
        return self.filter(
                    meetup=Meetup.objects.current()
                ).order_by('start_time')



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
    start_time = models.TimeField(
        null=True,
        verbose_name='Дата начала',
    )
    end_time = models.TimeField(
        null=True,
        verbose_name='Дата окончания',
    )
    is_finished = models.BooleanField(
        default=False,
    )


    objects = ReportManager()


    class Meta:
        verbose_name = 'доклад'
        verbose_name_plural = 'доклады'

    def __str__(self):
        return f'{self.theme}({self.speaker})'

    def set_speaker(self, speaker):
        self.speaker = speaker
        self.save()
        speaker.set_status(self.meetup, MemberStatus.SPEAKER)


    def set_finished(self):
        self.is_finished = True


class FeedbackManager(models.Manager):
    def current_question(self, id):
        return self.filter(
                    is_answered=False,
                    is_question=True,
                    report__id=id,
                ).order_by('id').first()

    def actual_questions(self):
        return self.filter(
                    is_answered=False,
                    is_question=True,
                    report=Report.objects.current_report()
                ).order_by('id')



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

    is_answered = models.BooleanField(
        'Дан ответ',
        default=False,
        db_index=True,
    )

    grade = models.CharField(
        'Оценка',
        max_length=1,
        choices=GRADES,

        blank=True
    )

    objects = FeedbackManager()


    class Meta:
        verbose_name = 'отклик'
        verbose_name_plural = 'отклики'

    def __str__(self):
        return f'{self.report}({self.member})'


    def set_answered(self):
        self.is_answered = True

    def set_grade(self, grade):
        if str(grade) in dict(self.GRADES).keys() and not self.grade:
            self.grade = str(grade)
            self.save()
            return True
        return False
