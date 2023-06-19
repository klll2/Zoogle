# Generated by Django 4.1 on 2023-06-19 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Zoo", "0018_alter_animal_anm_join_alter_animal_anm_last"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="anm_join",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 6, 19, 15, 22, 2, 834913),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="anm_last",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 6, 19, 15, 22, 2, 834913),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="anm_mc",
            field=models.CharField(default="Null", max_length=20),
        ),
    ]