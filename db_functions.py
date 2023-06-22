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
