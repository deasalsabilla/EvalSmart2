# Generated by Django 4.2.5 on 2024-11-28 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0009_alter_kriteria_bobot"),
    ]

    operations = [
        migrations.AddField(
            model_name="kriteria",
            name="tipe",
            field=models.CharField(
                choices=[("benefit", "Benefit"), ("cost", "Cost")],
                default="benefit",
                max_length=10,
            ),
        ),
    ]
