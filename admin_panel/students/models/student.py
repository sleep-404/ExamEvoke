import uuid

from django.db import models
from django.contrib.auth.models import User
from admin_panel.models.university.batch import Batch
from admin_panel.students.models.base import BaseUser
# from admin_panel.models.user.base import BaseUser


class Student(BaseUser):
    user = models.OneToOneField(
        User,
        related_name="student",
        on_delete=models.CASCADE
    )
    batch = models.ForeignKey(
        Batch,
        related_name="student",
        on_delete=models.CASCADE
    )
    grade = models.CharField(max_length=255)
    section = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    parent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    year_admitted = models.IntegerField(
        null=True,
        blank=True,
    )
    house = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    admission_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
