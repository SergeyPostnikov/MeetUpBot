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