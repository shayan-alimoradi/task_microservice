from django.core import mail
from django.test import TestCase
from django.utils import timezone

from task.models import Project, Task
from task.tasks import (
    send_due_task_reminders,
    send_daily_project_summary_report,
)


class TestCeleryTasks(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            description="Description of Test Project",
        )

        self.first_task = Task.objects.create(
            project=self.project,
            title="Task 1",
            description="Description of Task 1",
            status="completed",
            due_date=timezone.now() + timezone.timedelta(days=1),
        )

        self.second_task = Task.objects.create(
            project=self.project,
            title="Task 2",
            description="Description of Task 2",
            status="pending",
            due_date=timezone.now() + timezone.timedelta(hours=23),
        )

    def test_send_due_task_reminders(self):
        send_due_task_reminders.apply()

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Task Reminder", email.subject)

    def test_send_daily_project_summary_report(self):
        send_daily_project_summary_report.apply()

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(
            f"Daily Project Summary Report for {self.project.name}", email.subject
        )
        self.assertIn("Total Tasks: 2", email.body)
        self.assertIn("Completed Tasks: 1", email.body)
        self.assertIn("Pending Tasks: 1", email.body)
