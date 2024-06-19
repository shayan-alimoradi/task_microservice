from datetime import timedelta

from django.core.mail import send_mail
from django.utils.timezone import now
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

from .models import Task, Project


@shared_task
def send_due_task_reminders():
    due_soon = now() + timedelta(hours=24)
    tasks = Task.objects.select_related("project").filter(
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


@shared_task
async def send_daily_project_summary_report():
    projects = await sync_to_async(Project.objects.all, thread_sensitive=True)()

    for project in projects:
        # Collect project summary information asynchronously
        total_tasks = await sync_to_async(project.tasks.count, thread_sensitive=True)()
        completed_tasks = await sync_to_async(
            project.tasks.filter(status="completed").count, thread_sensitive=True
        )()
        pending_tasks = await sync_to_async(
            project.tasks.filter(status="pending").count, thread_sensitive=True
        )()

        subject = f"Daily Project Summary Report for {project.name}"
        message = f"""
        Project: {project.name}
        Total Tasks: {total_tasks}
        Completed Tasks: {completed_tasks}
        Pending Tasks: {pending_tasks}
        
        Add more project summary information as needed.
        """

        send_mail(
            subject,
            message,
            "shayan.aimoradii@gmail.com",
            ["shayan.aimoradii@gmail.com"],
            fail_silently=False,
        )

        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"Project summary report generated for {project.name}",
            },
        )
