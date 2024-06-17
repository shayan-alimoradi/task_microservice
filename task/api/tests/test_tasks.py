from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from task.models import Project, Task


class TaskTests(APITestCase):
    def setUp(self) -> None:
        self.project = baker.make(Project)
        self.task = baker.make(Task)

    def test_create_task_if_data_is_valid_returns_201(self):
        data = {
            "project": self.project.id,
            "title": "New task",
            "description": "Task description",
            "due_date": "2024-06-17",
        }
        response = self.client.post("/api/task-create/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_if_data_is_invalid_returns_400(self):
        response = self.client.post("/api/task-create/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tasks_returns_200(self):
        response = self.client.get("/api/tasks-list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_task_if_data_exists_returns_200(self):
        response = self.client.get(f"/api/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_if_data_is_valid_returns_200(self):
        data = {
            "project": self.project.id,
            "title": "New task",
            "description": "Task description",
            "due_date": "2024-06-17",
        }
        response = self.client.put(f"/api/task/{self.task.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task_returns_204(self):
        response = self.client.delete(f"/api/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskCachingTests(APITestCase):

    def setUp(self):
        self.task = baker.make(Task)
        self.project = baker.make(Project)

    def tearDown(self):
        cache.clear()

    def test_task_list_caching(self):
        response = self.client.get("/api/tasks-list/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("task_list" in cache)
        cached_response = cache.get("task_list")
        self.assertEqual(cached_response, response.data)

    def test_task_detail_caching(self):
        response = self.client.get(f"/api/task/{self.task.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"task_{self.task.id}"
        self.assertTrue(cache_key in cache)
        cached_response = cache.get(cache_key)
        self.assertEqual(cached_response, response.data)

    def test_task_cache_invalidation_on_update(self):
        response = self.client.put(
            f"/api/task/{self.task.id}/",
            data={
                "project": self.project.id,
                "title": "Updated Task",
                "description": "Updated Description",
                "due_date": "2024-06-17",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"task_{self.task.id}"
        self.assertIsNone(cache.get(cache_key))

    def test_task_cache_invalidation_on_delete(self):
        response = self.client.delete(f"/api/task/{self.task.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cache_key = f"task_{self.task.id}"
        self.assertIsNone(cache.get(cache_key))
