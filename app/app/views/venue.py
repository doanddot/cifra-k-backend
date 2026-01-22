from rest_framework import viewsets

from app.models import Venue
from app.permissions import IsSuperUser
from app.serializers import VenueSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    pagination_class = None
    permission_classes = [IsSuperUser]
