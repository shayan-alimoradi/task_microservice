from rest_framework import serializers

from ..models import Task, Comment


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id", 
            "project",
            "title",
            "created_at",
            "due_date",
        )


class TaskRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id", 
            "project",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
            "due_date",
        )
