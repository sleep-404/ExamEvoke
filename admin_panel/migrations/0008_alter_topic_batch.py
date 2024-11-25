# Generated by Django 5.0.4 on 2024-07-09 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0007_subject_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="batch",
            field=models.ForeignKey(
                help_text="The subject to which a topic belongs to",
                on_delete=django.db.models.deletion.CASCADE,
                to="admin_panel.batch",
            ),
        ),
    ]
