# Generated by Django 4.2.2 on 2024-08-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_mailing_send_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="auto_start",
            field=models.BooleanField(
                default=True, verbose_name="Автоматический старт"
            ),
        ),
    ]
