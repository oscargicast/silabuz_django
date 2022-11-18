"""
Reference:
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#specifying-custom-user-model
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'student'
        verbose_name = 'student'
        verbose_name_plural = 'student'