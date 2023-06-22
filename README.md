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

### Meetup
#### Менеджер запросов

- Meetup.objects.current() - возвращает ближайший митап(считаю его текущим)
- Meetup.objects.speakers() - возвращает список спикеров текущего митапа
- Meetup.objects.admins() - возвращает список админов текущего митапа
- Meetup.objects.donated_members() - возвращает список задонативших на текущий митап

#### Методы

- `.register_user(tg_id, status=MemberStatus.USER, tg_name='', name='')` - ищет пользователя по id telegram(`tg_id`), если не находит - создает нового в статусе `USER` или ином, если `status` не `None`, если заполнены параметры `tg_name` и `name`, то они тоже заполняются. Возвращает созданный/найденный объект класса `Member`.
- `.add_report(theme, start, end, speaker=None)` - ищет доклад по митапу и теме доклада(`theme`), если не находит - создает новый, с временем начала `start` и временем окончания `end`(передаются в виде строки 'HH:MM'), если указан `speaker`(объект класса `Member`, то он привязывается как докладчик, статус пользователя на докладе меняется на `SPEAKER`). Возвращает созданный/найденный объект класса `Report`.

### Member
#### Менеджер запросов

#### Методы

- `.donate(meetup)` - возвращает сумму доната пользователя, в качестве аргумента принимает объект класса `Meetup`.
- `.set_status(meetup, status)` - устанавливает пользователю статус на митапе, принимает объект класса `Meetup` и строку `status`.

### Report
#### Менеджер запросов

#### Методы

- `.set_speaker(speaker)` - принимает объект класса `Member`, привязывает его к докладу в качестве докладчика, статус пользователя на докладе меняется на `SPEAKER`.

### Пример работы

```python
current_meetup = Meetup.objects.current()
member = Meetup.objects.donated_members()[0]:
sum = member.donate(current_meetup)
```


