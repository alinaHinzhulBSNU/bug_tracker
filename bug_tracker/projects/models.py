from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from .enums import SEVERITY, STATUS
from .helpers import get_severity_by_code, get_status_by_code


class Project(models.Model):
    name = models.CharField(
        null=False,
        verbose_name="Name",
        max_length=200,
        validators=[validators.MinLengthValidator(2)])

    start_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Start time")

    end_time = models.DateTimeField(
        null=True,
        verbose_name="End time")

    description = models.TextField(
        null=False,
        verbose_name="Description",
        max_length=1000,
        validators=[validators.MinLengthValidator(2)])

    team = models.ManyToManyField(User,
                                  verbose_name="Team")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"
        verbose_name = "Project"
        ordering = ["start_time"]


class Task(models.Model):
    text = models.CharField(
        null=False,
        blank=False,
        verbose_name="Text",
        max_length=200,
        validators=[validators.MinLengthValidator(2)])

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Start time")

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="End time")

    severity = models.CharField(
        null=False,
        blank=False,
        max_length=2,
        verbose_name="Severity",
        choices=SEVERITY,
    )

    status = models.CharField(
        null=False,
        blank=False,
        max_length=2,
        verbose_name="Status",
        choices=STATUS,
    )

    project = models.ForeignKey(
        Project,
        null=False,
        blank=False,
        verbose_name="Project",
        on_delete=models.CASCADE,
    )

    performer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name="Performer",
        on_delete=models.CASCADE,
    )

    def get_severity(self):
        return get_severity_by_code(self.severity)

    def get_status(self):
        return get_status_by_code(self.status)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"
        ordering = ["start_time"]
