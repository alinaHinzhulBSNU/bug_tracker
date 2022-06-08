from django.contrib.auth.models import User
from django.db import models
from django.core import validators


# Create your models here.
class Project(models.Model):
    name = models.CharField(
        null=False,
        verbose_name='Name',
        max_length=200,
        validators=[validators.MinLengthValidator(2)])

    start_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Start time')

    end_time = models.DateTimeField(null=True,
                                    verbose_name='End time')

    description = models.TextField(
        null=False,
        verbose_name='Description',
        max_length=1000,
        validators=[validators.MinLengthValidator(2)])

    team = models.ManyToManyField(User,
                                  verbose_name="Team")

    # PRESENTATION
    def __str__(self):
        return "Name: " + self.name \
               + ", start time: " + str(self.start_time.strftime("%Y-%m-%d %H:%M:%S")) \
               + ", end time: " + str(self.end_time.strftime("%Y-%m-%d %H:%M:%S"))\
               + ", description: " + str(self.description)

    class Meta:
        verbose_name_plural = 'Projects'
        verbose_name = 'Project'
        ordering = ['start_time']
