# Generated by Django 5.0.1 on 2024-01-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta", "0002_alter_doi_options"),
        ("rt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="rtsimulation",
            name="DOI",
            field=models.ManyToManyField(blank=True, to="meta.doi"),
        ),
    ]