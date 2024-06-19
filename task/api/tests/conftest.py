import os

import pytest
from asgiref.sync import sync_to_async
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from task.models import Project, Task


@pytest.fixture
async def create_project():
    project = await sync_to_async(Project.objects.create)(
        name="Test Project",
        description="Test project description",
    )
    return project


@pytest.fixture
async def create_task(create_project):
    project = await create_project
    task = await sync_to_async(Task.objects.create)(
        project=project,
        title="Test Task",
        description="Test task description",
        due_date="2024-12-31",
    )
    return task
