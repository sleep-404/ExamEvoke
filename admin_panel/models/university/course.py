import uuid

from django.db import models

from admin_panel.models.university.organization import Organization


class Course(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        help_text="The school/college/organization to which the course belongs to",
    )
    course_id = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)
