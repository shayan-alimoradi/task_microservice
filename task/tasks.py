from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Task


@shared_task
def send_due_task_reminders():
    due_soon = now() + timedelta(hours=24)
    tasks = Task.objects.filter(
        due_date__lte=due_soon, due_date__gte=now(), status="pending"
    )

    for task in tasks:
        send_mail(
            "Task Reminder",
            f'Reminder: The task "{task.title}" is due soon.',
            "shayan.aimoradii@gmail.com",
            ["shayan.aimoradii@gmail.com"],
            fail_silently=False,
        )
