# Generated by Django 5.0.1 on 2024-03-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hydro", "0012_hydrosimulation1dmodelfile_interactive_plot_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hydrosimulation1dmodelfile",
            name="interactive_plot",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
