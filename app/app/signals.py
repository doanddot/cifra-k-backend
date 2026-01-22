from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver

from .models import Venue, VenueWeather, EventStatus, Event
from .tasks import send_event_email
from .utils import fetch_venue_weather


WIND_DIRS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]


@receiver(post_save, sender=Venue)
def update_or_create_venue_weather(sender, instance, created, **kwargs):
    if created:
        try:
            weather_data = fetch_venue_weather(instance.location)
            venue_weather, created = VenueWeather.objects.update_or_create(venue=instance, defaults=weather_data)
        except Exception as e:
            print(f"Ошибка при получении погоды для {instance.title}: {e}")


@receiver(pre_save, sender=Event)
def event_pre_save(sender, instance, **kwargs):
    instance._prev_status = sender.objects.get(pk=instance.pk).status


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, **kwargs):
    prev_status = getattr(instance, '_prev_status', EventStatus.DRAFT)
    if prev_status == EventStatus.DRAFT and instance.status == EventStatus.PUBLISHED:
        recipients = [
            'user1@example.com',
            'user2@example.com'
        ]
        subject = f"Event published: {instance.name}"
        message = f"The event '{instance.name}' is now published.\n\nDetails: {instance.description}"

        send_event_email.delay(recipients, subject, message)
