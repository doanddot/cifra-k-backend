from django.contrib.gis.db import models


class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(help_text='Название', max_length=255)
    location = models.PointField(help_text='Гео-координаты', srid=4326)


class VenueWeather(models.Model):
    id = models.AutoField(primary_key=True)
    venue = models.OneToOneField(Venue, on_delete=models.CASCADE, related_name='weather')
    temperature = models.FloatField(help_text="Температура в °C")
    humidity = models.FloatField(help_text="Влажность в %")
    pressure = models.FloatField(help_text="Атмосферное давление в мм рт. ст.")
    wind_speed = models.FloatField(help_text="Скорость ветра в м/с")
    wind_direction = models.CharField(max_length=10, help_text="Направление ветра (N, NE, E...)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
