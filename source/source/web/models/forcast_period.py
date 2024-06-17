from django.db import models

from web.models.location import Location


class ForcastPeriod(models.Model):
    class Meta:
        verbose_name = 'Weather forcast periods'

    number = models.IntegerField()
    name = models.CharField(max_length=16)
    location = models.ForeignKey(Location, related_name='weather_forcast_period',
                                 on_delete=models.CASCADE)
    is_daytime = models.BooleanField(default=False)
    temperature = models.IntegerField()
    temperature_unit = models.CharField(default='F', max_length=1)
    temperature_trend = models.CharField(max_length=32, null=True, blank=True, default=None)
    win_speed = models.CharField(max_length=32, null=True, blank=True, default=None)
    win_direction = models.CharField(max_length=8, null=True, blank=True, default=None)
    icon = models.CharField(max_length=255)
    short_forecast = models.CharField(max_length=255)
    detailed_forecast = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
