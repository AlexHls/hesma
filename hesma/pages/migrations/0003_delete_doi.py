# Generated by Django 5.0.1 on 2024-01-03 14:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hydro", "0006_remove_hydrosimulation_doi"),
        ("pages", "0002_doi"),
    ]

    operations = [
        migrations.DeleteModel(
            name="DOI",
        ),
    ]