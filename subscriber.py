import json
import os

import django
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from task.models import Project

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="project_rabbitmq", port=5672)
)
channel = connection.channel()
print("Connection: ", connection)

channel.queue_declare(queue="project_queue")


def callback(ch, method, properties, body):
    data = json.loads(body)
    print("data: ", data)

    if properties.content_type == "create_project":
        project = Project(
            id=data["id"],
            name=data["name"],
            description=data["description"],
        )
        project.save()


channel.basic_consume(
    queue="project_queue", on_message_callback=callback, auto_ack=True
)

print("Started Consuming")

channel.start_consuming()

channel.close()
