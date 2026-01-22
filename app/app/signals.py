from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from .models import Venue, VenueWeather
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
