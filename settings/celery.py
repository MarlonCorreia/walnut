"""
Walnut Celery config
"""

###
# Libraries
###
import os

from celery.utils.log import get_task_logger
from celery import Celery
from django.conf import settings

logger = get_task_logger(__name__)

###
# Main Configuration
###
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)