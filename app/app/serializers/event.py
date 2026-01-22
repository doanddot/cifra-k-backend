from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Event, Venue

from .venue import VenueSerializer

User = get_user_model()


class EventAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class EventSerializer(serializers.ModelSerializer):
    author = EventAuthorSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all(), source='venue', write_only=True)

    class Meta:
        model = Event
        fields = '__all__'