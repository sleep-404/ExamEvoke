# Generated by Django 5.0.4 on 2024-04-05 14:57

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("course_id", models.IntegerField()),
                ("course_name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("status", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Batch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("serial_no", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "course",
                    models.ForeignKey(
                        help_text="The course to which a batch belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_panel.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="organization",
            field=models.ForeignKey(
                help_text="The school/college/organization to "
                "which the course belongs to",
                on_delete=django.db.models.deletion.CASCADE,
                to="admin_panel.organization",
            ),
        ),
    ]
