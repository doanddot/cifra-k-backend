"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from app.views import EventViewSet, VenueViewSet, EventImportView


router = routers.DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    path("events/import/", EventImportView.as_view()),

    path('admin/', admin.site.urls),
    path("", include(router.urls)),

    path('openapi.json', SpectacularJSONAPIView.as_view(), name='openapi.json'),
    path('docs', SpectacularSwaggerView.as_view(url_name='openapi.json')),
    path('redoc', SpectacularRedocView.as_view(url_name='openapi.json')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
