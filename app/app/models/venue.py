from django.contrib.gis.db import models


class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(help_text='Название', max_length=255)
    location = models.PointField(help_text='Гео-координаты', srid=4326)
