from django.db import models

from admin_panel.models.university.organization import Organization
from django.contrib.auth.models import User

from admin_panel.students.models.base import BaseUser


class EmployeeRole(models.TextChoices):
    EVALUATOR = "EVALUATOR"
    SCANNER = "SCANNER"


class Employee(BaseUser):
    user = models.OneToOneField(
        User,
        related_name="employee",
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization,
        related_name="employees",
        on_delete=models.CASCADE
    )
    role = models.CharField(
        choices=EmployeeRole.choices,
        max_length=255,
        default=EmployeeRole.EVALUATOR,
    )
    signature_picture_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
