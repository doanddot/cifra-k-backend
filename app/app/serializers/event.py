from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import EventStatus, Event, Venue, EventImage

from .venue import VenueSerializer

User = get_user_model()


class EventAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventSerializer(serializers.ModelSerializer):
    author = EventAuthorSerializer(read_only=True)
    images = EventImageSerializer(many=True, read_only=True)
    new_images = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    status = serializers.CharField(read_only=True)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all(), source='venue', write_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        new_images = validated_data.pop('new_images', [])
        event = super().create(validated_data)

        for img in new_images:
            EventImage.objects.create(event=event, image=img)

        return event

    def update(self, instance, validated_data):
        new_images = validated_data.pop('new_images', None)
        event = super().update(instance, validated_data)

        if new_images is not None:
            instance.images.all().delete()
            for img in new_images:
                EventImage.objects.create(event=instance, image=img)

        return event