import datetime
import logging

from django.utils import timezone

from report.telegram import send_error_to_telegram_group
from weather.celery import app
from web.backends.helper import ApiHelper
from web.models.forcast_period import ForcastPeriod
from web.models.location import Location

logger = logging.getLogger('backend')


@app.task()
def schedule_location_periods():
    locations = Location.objects.all()
    current_time = timezone.localtime()
    delay = 1
    for location in locations:
        update_location_periods.apply_async(
            args=[location.pk, 'schedule'],
            eta=current_time + datetime.timedelta(seconds=delay * 0.2)
        )
        delay += 1


@app.task()
def schedule_location_grid_point():
    locations = Location.objects.all()
    current_time = timezone.localtime()
    delay = 1
    for location in locations:
        check_and_update_grid_point_change.apply_async(
            args=[location.pk, 'schedule'],
            eta=current_time + datetime.timedelta(seconds=delay * 0.2)
        )
        delay += 1


@app.task()
def update_location_periods(location_id, source=''):
    try:
        logger.info(f"[+] update_location_periods -> start",
                    extra=dict(location_id=location_id, source=source))
        location = Location.objects.get(pk=location_id)
        status, periods_raw_data = ApiHelper.get_weather_forcast_periods(location.grid_id,
                                                                         location.grid_x,
                                                                         location.grid_y)

        if status != 200:
            logger.error('[+] update_location_periods -> CAN NOT GET information from server')
            return False
        location.updated = periods_raw_data['properties']['updated']
        location.generated_at = periods_raw_data['properties']['generatedAt']
        location.update_time = periods_raw_data['properties']['updateTime']
        location.save()
        periods = periods_raw_data['properties']['periods']
        ForcastPeriod.objects.filter(location=location).delete()
        for period in periods:
            _obj = ForcastPeriod(
                location=location,
                number=period["number"],
                name=period["name"],
                is_daytime=period["isDaytime"],
                temperature=period["temperature"],
                temperature_unit=period["temperatureUnit"],
                temperature_trend=period["temperatureTrend"],
                win_speed=period["windSpeed"],
                win_direction=period["windDirection"],
                icon=period["icon"],
                short_forecast=period["shortForecast"],
                detailed_forecast=period["detailedForecast"],
            )
            _obj.save()
        logger.info(f"[+] update_location_periods -> finish",
                    extra=dict(location_id=location_id, source=source))
    except Exception as ex:
        logger.exception(f'[+] update_location_periods -> error', extra=dict(ex=ex))
        message = f'\nFunction: update_location_periods\nError:\n{ex}'
        send_error_to_telegram_group(message)


@app.task()
def check_and_update_grid_point_change(location_id, source=''):
    try:
        logger.info(f"[+] check_and_update_grid_point_change -> start",
                    extra=dict(location_id=location_id, source=source))
        location = Location.objects.get(pk=location_id)
        status, grid_point_raw_data = ApiHelper.get_grid_point_from_location(location.lat, location.long)
        if status != 200:
            logger.error(
                '[+] check_and_update_grid_point_change -> CAN NOT GET information from server')
            return None, None
        properties = grid_point_raw_data['properties']
        # Point
        grid_id = properties['gridId']
        grid_x = properties['gridX']
        grid_y = properties['gridY']
        if location.grid_id != grid_id or location.grid_x != grid_x or location.grid_y != grid_y:
            location.grid_id = grid_id
            location.grid_x = grid_x
            location.grid_y = grid_y
            location.save()
            update_location_periods.delay(location_id)
        logger.info(f"[+] check_and_update_grid_point_change -> finish",
                    extra=dict(location_id=location_id, source=source))
    except Exception as ex:
        logger.exception(f'[+] check_and_update_grid_point_change -> error', extra=dict(ex=ex))
        message = f'\nFunction: check_and_update_grid_point_change\nError:\n{ex}'
        send_error_to_telegram_group(message)
