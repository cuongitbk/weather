from django.test import TestCase

from web.backends.helper import ApiHelper

TEST_LAT = 41.7352
TEST_LONG = -111.8349
TEST_OFFICE_ID = 'SLC'
TEST_FORCAST_ZONE = 'UTZ107'
TEST_GRID_ID = 'SLC'
TEST_GRID_X = 108
TEST_GRID_Y = 219
TEST_CITY = 'Logan'
TEST_STATE = 'UT'


class TestApiHelper(TestCase):
    def test_get_grid_point_from_location_wrong_values(self):
        status, content = ApiHelper.get_grid_point_from_location(None, None)
        self.assertEqual(400, status)

    def test_get_grid_point_from_location_with_not_found_location(self):
        hanoi_lat = 21.0228
        hanoi_long = 105.7958
        status, content = ApiHelper.get_grid_point_from_location(hanoi_lat, hanoi_long)
        self.assertEqual(404, status)
        self.assertEqual('https://api.weather.gov/problems/InvalidPoint', content['type'])
        self.assertEqual(True, f'{hanoi_lat}' in content['detail'] and f'{hanoi_long}' in content['detail'])

    def test_get_grid_point_from_location(self):
        status, content = ApiHelper.get_grid_point_from_location(TEST_LAT, TEST_LONG)
        self.assertEqual(200, status)
        self.assertEqual(True, isinstance(content, dict) and 'properties' in content and 'geometry' in content)
        self.assertEqual(TEST_LONG, content['geometry']['coordinates'][0])
        self.assertEqual(TEST_LAT, content['geometry']['coordinates'][1])
        self.assertEqual(TEST_GRID_ID, content['properties']['gridId'])
        self.assertEqual(TEST_GRID_X, content['properties']['gridX'])
        self.assertEqual(TEST_GRID_Y, content['properties']['gridY'])

    def test_get_weather_forcast_periods(self):
        status, content = ApiHelper.get_weather_forcast_periods(TEST_GRID_ID, TEST_GRID_X, TEST_GRID_Y)
        self.assertEqual(200, status)
        self.assertEqual(True, isinstance(content, dict) and 'properties' in content)
        self.assertEqual(True, 'periods' in content['properties'])
        self.assertEqual(14, len(content['properties']['periods']))
        self.assertEqual(True, 'updated' in content['properties'])
        self.assertEqual(True, 'generatedAt' in content['properties'])
        self.assertEqual(True, 'updateTime' in content['properties'])

    def test_get_weather_forcast_periods_invalid_grid_id(self):
        status, content = ApiHelper.get_weather_forcast_periods('XXXXXX', TEST_GRID_X, TEST_GRID_Y)
        self.assertEqual(404, status)
        self.assertEqual(True, isinstance(content, dict) and 'parameterErrors' in content)
        self.assertEqual('path.wfo', content['parameterErrors'][0]['parameter'])
        self.assertEqual('https://api.weather.gov/problems/NotFound', content['type'])

    def test_get_weather_forcast_periods_invalid_grid_x(self):
        status, content = ApiHelper.get_weather_forcast_periods(TEST_GRID_ID, -TEST_GRID_X, TEST_GRID_Y)
        self.assertEqual(404, status)
        self.assertEqual(True, isinstance(content, dict) and 'parameterErrors' in content)
        self.assertEqual('path.x', content['parameterErrors'][0]['parameter'])
        self.assertEqual('https://api.weather.gov/problems/NotFound', content['type'])

    def test_get_weather_forcast_periods_invalid_grid_y(self):
        status, content = ApiHelper.get_weather_forcast_periods(TEST_GRID_ID, TEST_GRID_X, -TEST_GRID_Y)
        self.assertEqual(404, status)
        self.assertEqual(True, isinstance(content, dict) and 'parameterErrors' in content)
        self.assertEqual('path.y', content['parameterErrors'][0]['parameter'])
        self.assertEqual('https://api.weather.gov/problems/NotFound', content['type'])

    def test_get_forcast_office_info(self):
        status, content = ApiHelper.get_forcast_office_info(TEST_OFFICE_ID)
        self.assertEqual(200, status)
        self.assertEqual(True, isinstance(content, dict) and 'id' in content)
        self.assertEqual(TEST_OFFICE_ID, content['id'])
        self.assertEqual(True, 'name' in content and len(content['name']) > 0)
        self.assertEqual(True, 'telephone' in content and len(content['telephone']) > 0)
        self.assertEqual(True, 'faxNumber' in content and len(content['faxNumber']) > 0)
        self.assertEqual(True, 'email' in content and len(content['email']) > 0)
        self.assertEqual(True, 'nwsRegion' in content and len(content['nwsRegion']) > 0)
        self.assertEqual(True, 'parentOrganization' in content and len(content['parentOrganization']) > 0)

    def test_get_forcast_office_info_invalid_id(self):
        status, content = ApiHelper.get_forcast_office_info(f'XX{TEST_OFFICE_ID}')
        self.assertEqual(404, status)
        for error in content['parameterErrors']:
            self.assertEqual('path.officeId', error['parameter'])
        self.assertEqual('https://api.weather.gov/problems/NotFound', content['type'])

    def test_get_forcast_zone_info(self):
        status, content = ApiHelper.get_forcast_zone_info(TEST_FORCAST_ZONE)
        self.assertEqual(200, status)
        self.assertEqual(True, isinstance(content, dict) and 'properties' in content and 'geometry' in content)
        self.assertEqual(TEST_FORCAST_ZONE, 'id' in content['properties'] and content['properties']['id'])
        self.assertEqual(True, 'name' in content['properties'] and len(content['properties']['name']) > 0)
        self.assertEqual(True, 'coordinates' in content['geometry'] and len(content['geometry']['coordinates']) > 0)

    def test_get_forcast_zone_info_invalid_id(self):
        status, content = ApiHelper.get_forcast_zone_info(f'XXX{TEST_FORCAST_ZONE}')
        self.assertEqual(404, status)
        for error in content['parameterErrors']:
            self.assertEqual('path.zoneId', error['parameter'])
        self.assertEqual('https://api.weather.gov/problems/NotFound', content['type'])

