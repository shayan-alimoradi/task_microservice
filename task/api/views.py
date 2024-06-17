from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Task
from .serializers import (
    TaskListSerializer, 
    TaskRetrieveSerializer,
)


class TaskListAPIView(APIView):
    """
    Return a list of all tasks.
    The list is cached to reduce database load.
    """

    def get(self, request):
        cache_key = "task_list"
        if cache_key in cache:
            data = cache.get(cache_key)
        else:
            tasks = Task.objects.all()
            serializer = TaskListSerializer(tasks, many=True)
            data = serializer.data
            cache.set(cache_key, data)
        return Response(data)


class TaskCreateAPIView(APIView):
    """
    Create a new task.
    The cache is invalidated after creating a new task.

    Input data => { \n
        "project": "int" \n
        "title": "str", \n
        "description": "str", \n
        "due_date": "datetime"
    }
    """

    def post(self, request):
        serializer = TaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache after creating a new task
            cache.delete("task_list")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        """
        Retrieve the details of a specific task by its ID.

        Args:
            pk (int): The primary key of the task.
        """
        cache_key = f"task_{pk}"
        if cache_key in cache:
            data = cache.get(cache_key)
        else:
            task = self.get_object(pk)
            serializer = TaskRetrieveSerializer(task)
            data = serializer.data
            cache.set(cache_key, data)
        return Response(data)

    def put(self, request, pk):
        """
        Update the details of a specific task by its ID.
        The cache is invalidated after updating the task.

        Args:
            pk (int): The primary key of the task.

        Input data => { \n
            "project": "int", \n
            "title": "str", \n
            "description": "str", \n
            "due_date": "datetime"
        }
        """
        task = self.get_object(pk)
        serializer = TaskRetrieveSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache after updating task
            cache_key = f"task_{pk}"
            cache.delete(cache_key)
            cache.delete("task_list")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific task by its ID.
        The cache is invalidated after deleting the task.

        Args:
            pk (int): The primary key of the task.
        """
        task = self.get_object(pk)
        task.delete()
        # Invalidate cache after deleting task
        cache_key = f"task_{pk}"
        cache.delete(cache_key)
        cache.delete("task_list")
        return Response(status=status.HTTP_204_NO_CONTENT)
