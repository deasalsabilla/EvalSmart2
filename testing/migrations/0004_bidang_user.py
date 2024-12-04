# Generated by Django 4.2.5 on 2024-11-19 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("testing", "0003_alter_bidang_options_rename_nama_bidang_bidang_nama"),
    ]

    operations = [
        migrations.AddField(
            model_name="bidang",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bidangs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
