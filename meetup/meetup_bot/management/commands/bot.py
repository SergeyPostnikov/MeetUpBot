from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Запуск чат-бота'

    def handle(self, *args, **options):
        # переменные импортируем с файла настроек: settings.TG_BOT_KEY
        pass
