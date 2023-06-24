"""
WSGI config for meetup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from meetup.settings import env, BASE_DIR

path = env('PROJECT_ROOT', default=BASE_DIR)

if path not in sys.path:
   sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'meetup.settings'

application = get_wsgi_application()