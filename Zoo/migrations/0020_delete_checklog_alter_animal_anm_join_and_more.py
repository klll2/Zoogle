# Generated by Django 4.1 on 2023-06-22 06:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Zoo", "0019_alter_animal_anm_join_alter_animal_anm_last_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CheckLog",
        ),
        migrations.AlterField(
            model_name="animal",
            name="anm_join",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 6, 22, 15, 42, 0, 837961),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="anm_last",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 6, 22, 15, 42, 0, 837961),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="detaillog",
            name="anm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Zoo.animal"
            ),
        ),
    ]
