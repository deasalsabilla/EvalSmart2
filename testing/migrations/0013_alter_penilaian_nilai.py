# Generated by Django 4.2.5 on 2024-11-28 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0012_alter_penilaian_nilai"),
    ]

    operations = [
        migrations.AlterField(
            model_name="penilaian",
            name="nilai",
            field=models.TextField(blank=True, null=True),
        ),
    ]