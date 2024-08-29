from django.db import models
from main.utils import NULLABLE
from users.models import User


class Client(models.Model):
    email = models.EmailField(verbose_name="Почта", unique=True)
    first_name = models.CharField(max_length=200, **NULLABLE, verbose_name="Имя")
    last_name = models.CharField(max_length=200, **NULLABLE, verbose_name="Фамилия")
    comment = models.TextField(**NULLABLE, verbose_name="Комментарий")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)
        permissions = [
            ("can_view_clients", "can view clients"),
            ("can_change_clients", "can change clients"),
            ("can_delete_clients", "can delete clients"),
        ]

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField(verbose_name="Содержание")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="Owner",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)
        permissions = [
            ("can_change_message", "can change message"),
            ("can_delete_message", "can delete message"),
        ]

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    clients = models.ManyToManyField(
        Client,
        related_name="mailings",
        verbose_name="Клиент с почтой",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="mailings",
        verbose_name="massage",
    )
    send_date = models.DateTimeField(**NULLABLE, verbose_name="Дата начала рассылки")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания рассылки"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения рассылки"
    )
    is_active = models.BooleanField(default=True)

    COMPLETED = "completed"
    CREATED = "created"
    STARTED = "started"
    DAY = "once a day"
    MINUTE = "once a minute"
    WEEK = "once a week"
    MONTH = "once a month"
    STATUS = [(COMPLETED, "completed"), (CREATED, "created"), (STARTED, "started")]
    INTERVAL = [
        (MINUTE, "once a minute"),
        (DAY, "once a days"),
        (WEEK, "once a week"),
        (MONTH, "once a months"),
    ]

    interval = models.CharField(choices=INTERVAL, default=WEEK, verbose_name="Интервал")
    status = models.CharField(choices=STATUS, default=CREATED, verbose_name="Статус")
    end_date = models.DateTimeField(**NULLABLE, verbose_name="Дата окончания рассылки")
    auto_start = models.BooleanField(default=True, verbose_name="Автоматический старт")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("interval",)
        permissions = [
            ("can_change_mailing", "can change mailing"),
            ("can_delete_mailing", "can delete mailing"),
            ("can_view_mailing", "can view mailing"),
            ("can_create_mailing", "can create mailing"),
            ("can_switch_mailing", "can switch mailing"),
        ]

        def __str__(self):
            return f"Рассылка {self.pk}"


class TryMailing(models.Model):
    SUCCESS = "success"
    FAILURE = "failure"
    STATUSES = [(SUCCESS, "success"), (FAILURE, "failure")]
    last_try = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последней попытки"
    )
    status = models.CharField(choices=STATUSES, default=SUCCESS, verbose_name="Статус")
    response = models.TextField(**NULLABLE, verbose_name="Ответ")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("status",)

    def __str__(self):
        return f"{self.status}"
