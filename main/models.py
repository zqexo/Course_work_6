from django.db import models
from main.utils import NULLABLE
from users.models import User


class Client(models.Model):
    email = models.CharField(max_length=250, verbose_name="Почта")
    first_name = models.CharField(max_length=200, **NULLABLE, verbose_name="Имя")
    last_name = models.CharField(max_length=200, **NULLABLE, verbose_name="Фамилия")
    comment = models.TextField(**NULLABLE, verbose_name="Комментарий")
    users = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="Юзеры",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("email",)

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField(verbose_name="Содержание")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    email = models.ManyToManyField(
        Client,
        related_name="emails",
        verbose_name="Клиент с почтой",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="Сообщение",
        verbose_name="massage",
    )

    # Добавить поля: дата и время первой отправки рассылки (заполняются пользователем)
    send_date = models.CharField(
        max_length=200,
        **NULLABLE,
        default="Дата не указана",
        verbose_name="Дата отправки",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания рассылки"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения рассылки"
    )

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

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("interval",)

    def __str__(self):
        return f"Рассылка с клиентом {self.email} сообщением {self.message}"


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
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="emails",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("status",)

    def __str__(self):
        return f"{self.status}"
