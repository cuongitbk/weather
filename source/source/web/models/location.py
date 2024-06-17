from django.db import models

from web.models.forcast_office import ForcastOffice


class Location(models.Model):
    class Meta:
        verbose_name = 'Location'

    office = models.ForeignKey(ForcastOffice, related_name='location_office', on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    grid_id = models.CharField(max_length=8, db_index=True)
    grid_x = models.IntegerField(default=0)
    grid_y = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True, default=None)
    generated_at = models.DateTimeField(null=True, blank=True, default=None)
    update_time = models.DateTimeField(null=True, blank=True, default=None)
