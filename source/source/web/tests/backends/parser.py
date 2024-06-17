from django.test import TestCase

from web.backends.parser import ForcastDataParser
from web.models.forcast_office import ForcastOffice
from web.models.location import Location

TEST_LAT = 41.7352
TEST_LONG = -111.8349


class TestForcastDataParser(TestCase):
    def test_parse_wrong_values(self):
        location_count = Location.objects.count()
        office_count = ForcastOffice.objects.count()
        is_success = ForcastDataParser().parse(None, None)
        self.assertEqual(False, is_success)
        self.assertEqual(location_count, Location.objects.count())
        self.assertEqual(office_count, ForcastOffice.objects.count())

    def test_parse_with_not_found_location(self):
        hanoi_lat = 21.0228
        hanoi_long = 105.7958
        location_count = Location.objects.count()
        office_count = ForcastOffice.objects.count()
        is_success = ForcastDataParser().parse(hanoi_lat, hanoi_long)
        self.assertEqual(False, is_success)
        self.assertEqual(location_count, Location.objects.count())
        self.assertEqual(office_count, ForcastOffice.objects.count())

    def test_parse(self):
        location_count = Location.objects.count()
        office_count = ForcastOffice.objects.count()
        is_success = ForcastDataParser().parse(TEST_LAT, TEST_LONG)
        self.assertEqual(True, is_success)
        self.assertGreater(Location.objects.count(), location_count, 'Number of location is not changed')
        self.assertGreater(ForcastOffice.objects.count(), office_count, 'Number of office is not changed')
