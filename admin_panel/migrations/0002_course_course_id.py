# Generated by Django 5.0.4 on 2024-04-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="course_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
