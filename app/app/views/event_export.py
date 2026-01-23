from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from openpyxl import Workbook
from rest_framework.views import APIView

from app.models import Event
from app.permissions import IsSuperUser


@extend_schema(
    parameters=[
        OpenApiParameter("published_at_from", description="Дата публикации от", required=False),
        OpenApiParameter("published_at_to", description="Дата публикации до", required=False),
        OpenApiParameter("start_at_from", description="Дата начала от", required=False),
        OpenApiParameter("start_at_to", description="Дата начала до", required=False),
        OpenApiParameter("end_at_from", description="Дата окончания от", required=False),
        OpenApiParameter("end_at_to", description="Дата окончания до", required=False),
        OpenApiParameter("venue", description="ID места проведения", required=False),
        OpenApiParameter("rating_from", description="Рейтинг от", required=False),
        OpenApiParameter("rating_to", description="Рейтинг до", required=False),
    ]
)
class EventExportView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        queryset = Event.objects.all()

        published_from = request.GET.get("published_at_from")
        published_to = request.GET.get("published_at_to")
        start_from = request.GET.get("start_at_from")
        start_to = request.GET.get("start_at_to")
        end_from = request.GET.get("end_at_from")
        end_to = request.GET.get("end_at_to")
        venue_id = request.GET.get("venue")
        rating_from = request.GET.get("rating_from")
        rating_to = request.GET.get("rating_to")

        if published_from:
            queryset = queryset.filter(published_at__gte=parse_datetime(published_from))
        if published_to:
            queryset = queryset.filter(published_at__lte=parse_datetime(published_to))
        if start_from:
            queryset = queryset.filter(start_at__gte=parse_datetime(start_from))
        if start_to:
            queryset = queryset.filter(start_at__lte=parse_datetime(start_to))
        if end_from:
            queryset = queryset.filter(end_at__gte=parse_datetime(end_from))
        if end_to:
            queryset = queryset.filter(end_at__lte=parse_datetime(end_to))
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        if rating_from:
            queryset = queryset.filter(rating__gte=int(rating_from))
        if rating_to:
            queryset = queryset.filter(rating__lte=int(rating_to))

        wb = Workbook()
        ws = wb.active
        ws.title = "Events"

        ws.append([
            "name",
            "description",
            "published_at",
            "start_at",
            "end_at",
            "venue_name",
            "latitude",
            "longitude",
            "rating"
        ])

        for event in queryset:
            ws.append([
                event.name,
                event.description,
                localtime(event.published_at).replace(tzinfo=None),
                localtime(event.start_at).replace(tzinfo=None),
                localtime(event.end_at).replace(tzinfo=None),
                event.venue.title if event.venue else "",
                event.venue.location.y,
                event.venue.location.x,
                event.rating
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=events_export.xlsx"
        wb.save(response)

        return response