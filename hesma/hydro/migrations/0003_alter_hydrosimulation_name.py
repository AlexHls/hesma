# Generated by Django 4.1.9 on 2023-07-19 02:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hydro", "0002_alter_hydrosimulation_author_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hydrosimulation",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
