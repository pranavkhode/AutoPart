"""
WSGI config for auto_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_project.settings')


def initialize_database():
    if not os.environ.get('VERCEL') and not os.environ.get('NOW_REGION'):
        return

    try:
        call_command('migrate', verbosity=0, run_syncdb=True)
        from store.models import Part
        if Part.objects.count() == 0:
            call_command('seed_parts', verbosity=0)
    except Exception:
        pass


initialize_database()
application = get_wsgi_application()
