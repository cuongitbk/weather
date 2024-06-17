import logging

from django.conf import settings

from web.backends.connector import ApiConnector

logger = logging.getLogger('backend')


class ApiHelper:

    @classmethod
    def get_grid_point_from_location(cls, lat, long):
        # Round up to 4 decimals following https://weather-gov.github.io/api/general-faqs
        try:
            url = f'{settings.WEATHER_API_ENDPOINT}/points/{round(float(lat), 4)},{round(float(long), 4)}'
            return ApiConnector().get(url)
        except Exception as ex:
            logger.exception(f'[+] ApiHelper.get_grid_point_from_location -> error', extra=dict(ex=ex))
        return 400, None

    @classmethod
    def get_weather_forcast_periods(cls, grid_id, grid_x, grid_y):
        url = f'{settings.WEATHER_API_ENDPOINT}/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast'
        return ApiConnector().get(url)

    @classmethod
    def get_forcast_office_info(cls, office_id):
        url = f'{settings.WEATHER_API_ENDPOINT}/offices/{office_id}'
        return ApiConnector().get(url)

    @classmethod
    def get_forcast_zone_info(cls, zone_id):
        url = f'{settings.WEATHER_API_ENDPOINT}/zones/forecast/{zone_id}'
        return ApiConnector().get(url)
