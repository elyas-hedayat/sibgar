from django.conf import settings
from django.utils import timezone
from django.db import models

from ..common.models import TimeStampedModel

user = settings.AUTH_USER_MODEL


class Status(models.TextChoices):
    DRAFT = "پیش نویس", "پیش نویس"
    ACCEPTED = "تایید شده", "تایید شده"
    REJECTED = "رد شده", "رد شده"
    PUBLISHED = "منتشر شده", "منتشر شده"


class Article(TimeStampedModel):
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField()  # todo: add upload path
    publish_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=125, choices=Status.choices)

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    def __str__(self):
        return self.body[:50]
