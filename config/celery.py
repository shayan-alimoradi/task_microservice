from datetime import timedelta
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery = Celery("config")
celery.config_from_object("django.conf:settings", namespace="CELERY")

celery.conf.beat_schedule = {
    "task_reminder": {
        "task": "task.tasks.send_due_task_reminders",
        "schedule": timedelta(hours=1),
    },
    "daily_project_summary_reports": {
        "task": "task.tasks.send_daily_project_summary_report",
        "schedule": timedelta(days=1),
    },
}

celery.autodiscover_tasks()
