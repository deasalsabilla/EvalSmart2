# Generated by Django 4.2.5 on 2024-11-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0008_kriteria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kriteria",
            name="bobot",
            field=models.FloatField(default=0),
        ),
    ]
