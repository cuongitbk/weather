import datetime

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from background.cron_jobs import update_location_periods
from report.telegram import send_error_to_telegram_group
from web.models.forcast_period import ForcastPeriod
from web.models.location import Location


@cache_page(settings.INDEX_VIEW_CACHE_TIME, key_prefix="index_view")
def index(request):
    location_id = request.GET.get('id', None)
    if location_id is None:
        location_id = settings.DEFAULT_LOCATION_ID
    try:
        location = Location.objects.get(id=location_id)
    except Exception as ex:
        location = Location.objects.first()
        message = f'\nFunction: index with location_id={location_id}\nError:\n{ex}'
        send_error_to_telegram_group(message)
    # Force update periods for this location
    if location.updated_at + datetime.timedelta(seconds=settings.INDEX_VIEW_CACHE_TIME) < timezone.now():
        # Prevent too much tasks
        location.save()
        update_location_periods.delay(location_id, 'index')
    context = {
        'locations': Location.objects.all(),
        'location': location,
        'periods': ForcastPeriod.objects.filter(location=location).order_by('number')
    }
    return render(request, 'web/index.html', context)
