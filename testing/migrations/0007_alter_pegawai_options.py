# Generated by Django 4.2.5 on 2024-11-25 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0006_pegawai"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pegawai",
            options={"ordering": ["nama"], "verbose_name_plural": "Pegawai"},
        ),
    ]
