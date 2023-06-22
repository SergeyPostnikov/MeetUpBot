from django.core.management.base import BaseCommand
from django.conf import settings
from meetup_bot.models import Meetup, MemberStatus, Member


class Command(BaseCommand):
    help = 'Запуск чат-бота'

    def handle(self, *args, **options):
        pass
