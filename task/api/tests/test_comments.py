from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from task.models import Task, Comment


class CommentTests(APITestCase):
    def setUp(self) -> None:
        self.task = baker.make(Task)
        self.comment = baker.make(Comment)

    def test_create_comment_if_data_is_valid_returns_201(self):
        data = {
            "task": self.task.id,
            "author": "Corey",
            "content": "Test content",
        }
        response = self.client.post(
            f"/api/task/{self.task.id}/create-comment/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment_if_data_is_invalid_returns_400(self):
        response = self.client.post(
            f"/api/task/{self.task.id}/create-comment/", data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_comment_returns_200(self):
        response = self.client.get(f"/api/task/{self.task.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TaskCachingTests(APITestCase):

    def setUp(self):
        self.task = baker.make(Task)
        self.comment = baker.make(Comment)

    def tearDown(self):
        cache.clear()

    def test_task_list_caching(self):
        response = self.client.get(f"/api/task/{self.task.id}/comments/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(f"task_{self.task.id}_comments" in cache)
        cached_response = cache.get(f"task_{self.task.id}_comments")
        self.assertEqual(cached_response, response.data)

    def test_comment_cache_invalidation_on_create(self):
        response = self.client.post(
            f"/api/task/{self.task.id}/create-comment/",
            data={
                "task": self.task.id,
                "author": "Corey",
                "content": "Test content",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cache_key = f"task_{self.task.id}_comments"
        self.assertIsNone(cache.get(cache_key))
