import os, sys

import django
DJANGO_PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meetup.settings")
django.setup()

from meetup_bot.models import Meetup, MemberStatus, Member, Report, Feedback


def search_user(tg_name):
    return Member.objects.filter(tg_name=tg_name)


def add_new_user(name, tg_name, tg_id):
    Member.objects.create(tg_name=tg_name, name=name, tg_id=tg_id)


def search_meetup(date):
    return Meetup.objects.filter(date__gte=date)


def enroll_meetup(id, tg_id):
    meetup = Meetup.objects.filter(id=id)[0]
    meetup.register_user(tg_id)
    return meetup.theme, meetup.date


def get_status(tg_id, meetup):
    member = Member.objects.filter(tg_id=tg_id)[0]
    return member.get_status(meetup)


def get_meetup_users(tg_id):
    users = Meetup.objects.users() | Meetup.objects.speakers()
    return users.filter(job__gt='').exclude(tg_id=tg_id)

def add_user_info(tg_name, job, about):
    member = Member.objects.filter(tg_name=tg_name)
    member.update(job=job, about=about)

def search_speakers(tg_id):
    return Meetup.objects.speakers().exclude(tg_id=tg_id)

def get_current_report():
    return Report.objects.current_report()

def send_feedback(tg_id, text, report_id, is_questions=True):
    member = Member.objects.filter(tg_id=tg_id)[0]
    report = None
    if report_id:
        report = Report.objects.get(id=report_id)
    member.send_feedback(text, report, is_questions)

def get_reports(tg_id=None):
    if not tg_id:
        reports = Report.objects.actual_reports()
    else:
        reports = Report.objects.actual_reports().filter(speaker__tg_id=tg_id)
    return reports

def set_finished(report_id):
    report = Report.objects.filter(id=report_id)
    report.update(is_finished=True)

def get_current_question(report_id):
    return Feedback.objects.current_question(report_id)

def set_answered(question_id):
    print(question_id)
    question = Feedback.objects.filter(id=question_id)
    print(question)
    question.update(is_answered=True)


