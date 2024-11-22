from django.db import models

from admin_panel.models.university.organization import Organization
from admin_panel.models.user.base import BaseUser
from django.contrib.auth.models import User


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
