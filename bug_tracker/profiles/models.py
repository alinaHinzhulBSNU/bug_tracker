from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True)
    ROLE = (
        ('T', 'Tester'),
        ('D', 'Developer'),
        ('M', 'Manager'),
    )
    role = models.CharField(
        null=False,
        verbose_name='Favorite genre',
        max_length=2,
        choices=ROLE,
    )