from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from task.models import Task, Project


class ProjectCachingTests(APITestCase):

    def setUp(self):
        self.project = baker.make(Project)
        self.task = baker.make(Task)

    def tearDown(self):
        cache.clear()

    def test_task_list_caching(self):
        response = self.client.get("/api/tasks-list/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("task_list" in cache)
        cached_response = cache.get("task_list")
        self.assertEqual(cached_response, response.data)

    def test_task_cache_invalidation_on_update(self):
        response = self.client.put(
            f"/api/task/{self.task.id}/",
            data={
                "project": self.project.id,
                "title": "Updated Project", 
                "description": "Updated Description",
                "due_date": "2014-06-19"
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