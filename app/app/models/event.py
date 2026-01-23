from PIL import Image

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .venue import Venue


class EventStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(help_text='Название', max_length=255)
    thumbnail = models.ImageField('Превью-изображение', null=True, blank=True)
    description = models.TextField(help_text='Описание')
    published_at = models.DateTimeField(help_text='Дата и время публикации')
    start_at = models.DateTimeField(help_text='Дата и время начала проведения')
    end_at = models.DateTimeField(help_text='Дата и время завершения проведения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Автор')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='events', help_text='Место проведения')
    rating = models.PositiveSmallIntegerField(
        help_text='Рейтинг',
        validators = [MinValueValidator(0), MaxValueValidator(25)]
    )
    status = models.CharField(max_length=9, choices=EventStatus.choices, default=EventStatus.DRAFT, help_text='Статус')

    def clean(self):
        if self._state.adding and self.status == EventStatus.DRAFT:
            raise ValidationError("Нельзя создавать событие сразу со статусом 'published'")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.thumbnail:
            image = Image.open(self.thumbnail)
            image.thumbnail((min(image.size), 200))
            image.save(self.thumbnail.path)


class EventImage(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
