# Generated by Django 5.0.1 on 2024-03-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0005_contactmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="sticky",
            field=models.BooleanField(default=False),
        ),
    ]
