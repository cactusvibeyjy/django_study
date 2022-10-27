# Generated by Django 4.1.2 on 2022-10-27 12:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp03", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("writer", models.CharField(max_length=50)),
                ("content", models.TextField()),
                (
                    "post_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp03.board"
                    ),
                ),
            ],
        ),
    ]
