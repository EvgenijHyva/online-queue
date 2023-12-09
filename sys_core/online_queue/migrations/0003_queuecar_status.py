# Generated by Django 4.2.7 on 2023-12-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("online_queue", "0002_remove_queuecar_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="queuecar",
            name="status",
            field=models.CharField(
                choices=[
                    ("A", "Added"),
                    ("S", "Started"),
                    ("C", "Canceled"),
                    ("D", "Done"),
                ],
                default="A",
                max_length=1,
                verbose_name="status",
            ),
        ),
    ]
