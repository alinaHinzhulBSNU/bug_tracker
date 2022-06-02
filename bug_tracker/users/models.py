from django.db import models
from django.contrib.auth.models import User
from .enums import ROLE


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True)
    role = models.CharField(
        null=False,
        verbose_name='Favorite genre',
        max_length=2,
        choices=ROLE,
    )
