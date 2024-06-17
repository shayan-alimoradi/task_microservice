# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task, Comment

channel_layer = get_channel_layer()


@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": f"Task {instance.title} was {action}.",
        },
    )


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {"type": "send_notification", "message": f"Task {instance.title} was deleted."},
    )


@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"New comment by {instance.author} on task {instance.task.title}.",
            },
        )
