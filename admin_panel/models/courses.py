from django.db import models


class Course(models.Model):
    id = models.UUIDField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)
