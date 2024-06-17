from django.contrib import admin

from web.models.forcast_office import ForcastOffice
from web.models.forcast_period import ForcastPeriod
from web.models.location import Location


class ForcastOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'office_id',)


class ForcastPeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_name', 'name', 'number', 'is_daytime')
    ordering = ('location', 'number', )

    def location_name(self, obj):
        if obj.location:
            return f'{obj.location.city}, {obj.location.state}'
        return '---'


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'office_name', 'city', 'state', 'lat', 'long')

    def office_name(self, obj):
        if obj.office:
            return obj.office.name
        return '---'


# Register your models here.
admin.site.register(ForcastOffice, ForcastOfficeAdmin)
admin.site.register(ForcastPeriod, ForcastPeriodAdmin)
admin.site.register(Location, LocationAdmin)
