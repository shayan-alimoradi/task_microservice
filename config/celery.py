from datetime import timedelta
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery = Celery("config")
celery.config_from_object("django.conf:settings", namespace="CELERY")

celery.conf.beat_schedule = {
    "task_reminder": {
        "task": "task.tasks.send_due_task_reminders",
        "schedule": timedelta(seconds=30),
    },
}

celery.autodiscover_tasks()
