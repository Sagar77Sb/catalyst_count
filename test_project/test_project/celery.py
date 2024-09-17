# test_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

app = Celery('test_project')

# Load settings from Django's settings.py with CELERY_ prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps.
app.autodiscover_tasks()

