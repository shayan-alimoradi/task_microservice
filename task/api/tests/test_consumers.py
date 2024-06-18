import pytest
from channels.testing import WebsocketCommunicator
from asgiref.sync import sync_to_async

from task.asgi import application
from task.models import Task


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_websocket_connect():
    communicator = WebsocketCommunicator(application, "/ws/notifications/")
    connected, subprotocol = await communicator.connect()
    assert connected

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_task_created_notification(create_project):
    project = await create_project
    communicator = WebsocketCommunicator(application, "/ws/notifications/")
    connected, subprotocol = await communicator.connect()
    assert connected

    new_task = await sync_to_async(Task.objects.create)(
        project=project,
        title="New Task",
        description="A new task",
        due_date="2024-12-31",
    )

    response = await communicator.receive_json_from()
    assert response["message"] == f"Task {new_task.title} was created."

    await communicator.disconnect()
