import uuid

from django.db import models


class UserGender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"


class BaseUser(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(choices=UserGender.choices, max_length=20)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    telephone_number = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    profile_picture_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
