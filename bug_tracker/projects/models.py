from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from .enums import REPRODUCIBILITY, SEVERITY, PRIORITY, SYMPTOM, STATUS
from .helpers import \
    get_severity_by_code, \
    get_status_by_code, \
    get_reproducibility_by_code, \
    get_priority_by_code, \
    get_symptom_by_code


class Project(models.Model):
    name = models.CharField(
        null=False,
        verbose_name="Name",
        max_length=200,
        validators=[validators.MinLengthValidator(2)],
    )

    description = models.TextField(
        null=False,
        verbose_name="Description",
        max_length=1000,
        validators=[validators.MinLengthValidator(2)],
    )

    team = models.ManyToManyField(
        User,
        verbose_name="Team",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"
        verbose_name = "Project"


class Task(models.Model):
    text = models.CharField(
        null=False,
        blank=False,
        verbose_name="Text",
        max_length=200,
        validators=[validators.MinLengthValidator(2)],
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Start time",
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="End time",
    )

    severity = models.IntegerField(
        null=False,
        blank=False,
        default=1,
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
        null=True,
        blank=True,
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


class Bug(models.Model):
    summary = models.CharField(
        null=False,
        blank=False,
        verbose_name="Summary",
        max_length=200,
        validators=[validators.MinLengthValidator(2)],
    )

    description = models.TextField(
        null=False,
        blank=False,
        verbose_name="Description",
        validators=[validators.MinLengthValidator(2)],
    )

    reproducibility = models.CharField(
        null=False,
        blank=False,
        max_length=2,
        verbose_name="Reproducibility",
        choices=REPRODUCIBILITY
    )

    severity = models.IntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name="Severity",
        choices=SEVERITY,
    )

    priority = models.CharField(
        null=False,
        blank=False,
        max_length=2,
        verbose_name="Priority",
        choices=PRIORITY,
    )

    symptom = models.CharField(
        null=False,
        blank=False,
        max_length=3,
        verbose_name="Symptom",
        choices=SYMPTOM,
    )

    workaround = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Workaround",
    )

    first_screenshot = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Screenshot #1",
        upload_to="images/",
    )

    second_screenshot = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Screenshot #2",
        upload_to="images/",
    )

    third_screenshot = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Screenshot #3",
        upload_to="images/",
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Start time",
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="End time",
    )

    status = models.CharField(
        null=False,
        blank=False,
        max_length=2,
        verbose_name="Status",
        choices=STATUS,
    )

    performer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name="Performer",
        on_delete=models.CASCADE,
    )

    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        verbose_name="Project",
        on_delete=models.CASCADE,
    )

    def get_reproducibility(self):
        return get_reproducibility_by_code(self.reproducibility)

    def get_severity(self):
        return get_severity_by_code(self.severity)

    def get_priority(self):
        return get_priority_by_code(self.priority)

    def get_symptom(self):
        return get_symptom_by_code(self.symptom)

    def get_status(self):
        return get_status_by_code(self.status)

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name_plural = "Bugs"
        verbose_name = "Bug"
        ordering = ["start_time"]
