# Generated by Django 5.0.1 on 2024-01-04 09:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meta", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="doi",
            options={"ordering": ["-created"], "verbose_name": "DOI"},
        ),
    ]
