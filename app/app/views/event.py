from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets

from app.models import EventStatus, Event
from app.permissions import IsSuperUserOrReadOnly
from app.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'start_at': ['gte', 'lte'],
        'end_at': ['gte', 'lte'],
        'venue': ['exact'],
        'rating': ['exact']
    }
    search_fields = ['name', 'venue__title']
    ordering_fields = ['name', 'start_at', 'end_at']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Event.objects.all()

        return Event.objects.filter(status=EventStatus.PUBLISHED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(request={'multipart/form-data': EventSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(request={'multipart/form-data': EventSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request={'multipart/form-data': EventSerializer})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)