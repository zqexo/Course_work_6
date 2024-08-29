from django.db import models
from django.utils import timezone

from main.utils import NULLABLE
from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to="blog_images/", **NULLABLE, verbose_name="Изображение"
    )
    views = models.PositiveIntegerField(default=0)
    publish_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["-publish_date"]
        permissions = [
            ("can_create_blogpost", "can create blogpost"),
            ("can_update_blogpost", "can update blogpost"),
            ("can_delete_blogpost", "can delete blogpost"),
        ]

    def __str__(self):
        return self.title
