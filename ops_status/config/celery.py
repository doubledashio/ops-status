from __future__ import absolute_import
import os
import sys
import environ

from celery import Celery
from django.conf import settings  # noqa

ROOT_DIR = environ.Path(__file__) - 2  # (project/config/celery.py - 2 = /app)
PROJECT_DIR = ROOT_DIR.path('project')

sys.path.append(str(PROJECT_DIR))
sys.path.append(str(PROJECT_DIR.path('apps')))

env = environ.Env()
# environ.Env.read_env(str(ROOT_DIR.path('.env')))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

app = Celery('project')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
