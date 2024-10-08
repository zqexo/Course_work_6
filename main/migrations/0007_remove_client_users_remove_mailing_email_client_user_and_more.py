# Generated by Django 4.2.2 on 2024-08-28 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0006_alter_mailing_auto_start"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="users",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="email",
        ),
        migrations.AddField(
            model_name="client",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="User",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="clients",
            field=models.ManyToManyField(
                related_name="mailings",
                to="main.client",
                verbose_name="Клиент с почтой",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="Owner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Почта"),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mailings",
                to="main.message",
                verbose_name="massage",
            ),
        ),
    ]
