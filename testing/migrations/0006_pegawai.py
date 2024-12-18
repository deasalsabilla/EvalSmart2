# Generated by Django 4.2.5 on 2024-11-25 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0005_remove_bidang_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pegawai",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nomor_induk", models.CharField(max_length=20, unique=True)),
                ("nama", models.CharField(max_length=100)),
                ("alamat", models.TextField()),
                ("no_telp", models.CharField(max_length=15)),
                (
                    "bidang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="testing.bidang"
                    ),
                ),
            ],
        ),
    ]
