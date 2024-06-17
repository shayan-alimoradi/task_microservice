from django.urls import path

from . import views

app_name = "api_task"


urlpatterns = [
    path("tasks-list/", views.TaskListAPIView.as_view(), name="task-list"),
    path(
        "task-create/", views.TaskCreateAPIView.as_view(), name="task-create"
    ),
    path(
        "task/<int:pk>/",
        views.TaskDetailAPIView.as_view(),
        name="task-detail",
    ),
]
