# Generated by Django 5.0.4 on 2024-08-14 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0018_alter_employee_user_alter_student_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employees",
                to="admin_panel.organization",
            ),
            preserve_default=False,
        ),
    ]
