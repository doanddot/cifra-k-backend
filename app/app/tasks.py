from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Event, Venue, VenueWeather
from .utils import fetch_venue_weather


@shared_task(bind=True)
def send_event_email(self, recipients, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@example.com',
            recipient_list=recipients,
            fail_silently=False,
        )
        return {'recipients': recipients, 'subject': subject, 'status': 'sent'}
    except Exception as e:
        raise e


@shared_task
def publish_scheduled_events():
    now = timezone.now()
    events = Event.objects.filter(status='draft', published_at__lte=now)

    published = []

    for event in events:
        event.status = 'published'
        event.save()

        published.append(event.id)

    return published

@shared_task
def update_venue_weather():
    updated = []
    for venue in Venue.objects.all():
        try:
            weather_data = fetch_venue_weather(venue.location)
            venue_weather, created = VenueWeather.objects.update_or_create(venue=venue, defaults=weather_data)

            updated.append(venue.id)
        except Exception as e:
            print(f"Ошибка при получении погоды для {venue.title}: {e}")

    return updated