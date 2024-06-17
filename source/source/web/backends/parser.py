import datetime
import logging

from django.utils import timezone

from background.cron_jobs import update_location_periods
from report.telegram import send_error_to_telegram_group
from web.backends.helper import ApiHelper
from web.models.forcast_office import ForcastOffice
from web.models.location import Location

logger = logging.getLogger('backend')


class ForcastDataParser:
    grid_point = None
    relative_location = None
    zone_id = None

    def __parse_zone_locations(self, zone_id):
        try:
            status, zone_raw_data = ApiHelper.get_forcast_zone_info(zone_id)
            if status != 200:
                logger.error('[ForcastDataParser.__parse_zone_locations] '
                             'Error while getting zone information from server')
                return False
            coordinates = zone_raw_data['geometry']['coordinates'][0]
            for coordinate in coordinates:
                self.__parse_grid_point_info(coordinate[1], coordinate[0])
            logger.info(f'[ForcastDataParser.__parse_zone_locations] Complete zone={zone_id}')
            return True
        except Exception as ex:
            logger.exception(f'[ForcastDataParser.__parse_zone] --> ex={ex}')
            message = f'\nFunction: ForcastDataParser.__parse_zone_locations\nError:\n{ex}'
            send_error_to_telegram_group(message)
        return False

    def __parse_office(self, office_id):
        try:
            office = ForcastOffice.objects.filter(office_id=office_id).first()
            if not office:
                status, raw_data = ApiHelper.get_forcast_office_info(office_id)
                if status != 200:
                    logger.error('[ForcastDataParser.__parse_office] Error while getting office information from server')
                    return False
                office = ForcastOffice.objects.create(
                    type=raw_data['@type'],
                    name=raw_data['name'],
                    office_id=office_id,
                    telephone=raw_data['telephone'],
                    fax_number=raw_data['faxNumber'],
                    email=raw_data['email'],
                    nws_region=raw_data['nwsRegion'],
                    parent_organization=raw_data['parentOrganization'],
                )
                logger.info(f'[ForcastDataParser.__parse_office] Complete office={office_id}')
            return office
        except Exception as ex:
            logger.exception(f'[ForcastDataParser.__parse_office] --> ex={ex}')
            message = f'\nFunction: ForcastDataParser.__parse_office\nError:\n{ex}'
            send_error_to_telegram_group(message)
        return None

    def __parse_grid_point_info(self, lat, long):
        try:
            status, grid_point_raw_data = ApiHelper.get_grid_point_from_location(lat, long)
            if status != 200:
                logger.error('[ForcastDataParser.__parse_grid_point_info] '
                             'Error while getting grid point information from server')
                return None, None
            properties = grid_point_raw_data['properties']
            # Point
            grid_id = properties['gridId']
            grid_x = properties['gridX']
            grid_y = properties['gridY']
            # Location
            office_id = properties['gridId']
            office = self.__parse_office(office_id)
            if not office:
                return None, None
            city = properties['relativeLocation']['properties']['city']
            state = properties['relativeLocation']['properties']['state']
            lat = properties['relativeLocation']['geometry']['coordinates'][1]
            long = properties['relativeLocation']['geometry']['coordinates'][0]
            location = Location.objects.filter(office=office, city=city, state=state).first()
            if location:
                location.grid_id = grid_id
                location.grid_x = grid_x
                location.grid_y = grid_y
                location.lat = lat
                location.long = long
                location.save()
            else:
                location = Location.objects.create(
                    city=city,
                    state=state,
                    office=office,
                    grid_id=grid_id,
                    grid_x=grid_x,
                    grid_y=grid_y,
                    lat=lat,
                    long=long,
                )
            logger.info(f'[ForcastDataParser.__parse_grid_point_info] Complete point=({lat}, {long})')
            zone_id = properties['forecastZone'].split('/')[-1]
            return zone_id, location
        except Exception as ex:
            logger.exception(f'[ForcastDataParser.__parse_grid_point_info] --> ex={ex}')
            message = f'\nFunction: ForcastDataParser.__parse_grid_point_info\nError:\n{ex}'
            send_error_to_telegram_group(message)
        return None, None

    def parse(self, lat, long):
        zone_id, location = self.__parse_grid_point_info(lat, long)
        if not zone_id or not location:
            return False
        if not self.__parse_zone_locations(zone_id):
            return False
        locations = Location.objects.all()
        current_time = timezone.localtime()
        delay = 1
        for item in locations:
            update_location_periods.apply_async(
                args=[item.pk],
                eta=current_time + datetime.timedelta(seconds=delay * 0.5)
            )
        return True
