from drf_spectacular.utils import extend_schema_field
from django.contrib.gis.geos.point import Point
from rest_framework import serializers

from app.models import Venue


class VenueLocationSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

@extend_schema_field(VenueLocationSerializer)
class VenueLocationField(serializers.Field):

    def to_representation(self, value: Point):
        if not value:
            return None

        return { "lat": value.y, "lng": value.x, }

    def to_internal_value(self, data):
        try:
            return Point(float(data["lng"]), float(data["lat"]), srid=4326)
        except (KeyError, TypeError, ValueError):
            raise serializers.ValidationError("Location must be {'lat': float, 'lng': float }")


class VenueSerializer(serializers.ModelSerializer):
    location = VenueLocationField()

    class Meta:
        model = Venue
        fields = '__all__'
