# MeetUpBot
Имена переменных окружения. Если будут нужны какие-то ещё, сразу имена добавляем сюда.

TG_BOT_KEY=
PAYMENTS_TOKEN=
TG_ADMIN_ID=
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=
PROJECT_ROOT=

Для создания файла `.env` выполните команду:

```bash
$ cp example.env .env
```

переменные присваиваем в settings.py и импортируем в приложение:

```python
from django.conf import settings

settings.TG_BOT_KEY
```

## Менеджеры запросов и методы классов

Meetup.objects.current() - получить ближайший митап(считаю его текущим)
Meetup.objects.speakers() - список спикеров текущего митапа
Meetup.objects.admins() - список админов текущего митапа
Meetup.objects.donated_members() - список задонативших на текущий митап
Метод класса Member donate(meetup), возвращает сумму доната пользователя, в качестве аргумента принимает митап.

Пример работы:
```python
current_meetup = Meetup.objects.current()
member = Meetup.objects.donated_members()[0]:
sum = member.donate(current_meetup)
```


