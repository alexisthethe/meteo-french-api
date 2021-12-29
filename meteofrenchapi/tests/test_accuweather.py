import unittest

from meteofrenchapi.core import accuweather
from meteofrenchapi.tests import LAT_TEST, LONG_TEST


class TestAccuweather(unittest.TestCase):

    def test_base_get(self):
        test_endpoint = "/locations/v1/regions"
        res = accuweather.base_get(test_endpoint)
        assert(res.ok)
        params = {"language": "fr-fr"}
        res = accuweather.base_get(test_endpoint, params)
        assert(res.ok)

    def test_get_location_key(self):
        location_key = accuweather.get_location_key(LAT_TEST, LONG_TEST)
        assert(location_key == "2608429")

    def test_convert_to_m(self):
        # test convertion from mm
        valueobj = {'Metric': {'Value': 2.1, 'Unit': 'mm', 'UnitType': 3}, 'Imperial': {'Value': 0.0, 'Unit': 'in', 'UnitType': 1}}
        value = accuweather.convert_to_m(valueobj)
        assert(value == 0.0021)
        # test convertion from cm
        valueobj = {'Metric': {'Value': 2.1, 'Unit': 'cm', 'UnitType': 4}, 'Imperial': {'Value': 0.0, 'Unit': 'in', 'UnitType': 1}}
        value = accuweather.convert_to_m(valueobj)
        assert(value == 0.021)
        # test convertion from m
        valueobj = {'Metric': {'Value': 2.1, 'Unit': 'm', 'UnitType': 5}, 'Imperial': {'Value': 0.0, 'Unit': 'in', 'UnitType': 1}}
        value = accuweather.convert_to_m(valueobj)
        assert(value == 2.1)
        # test convertion from km
        valueobj = {'Metric': {'Value': 2.1, 'Unit': 'km', 'UnitType': 6}, 'Imperial': {'Value': 0.0, 'Unit': 'in', 'UnitType': 1}}
        value = accuweather.convert_to_m(valueobj)
        assert(value == 2100)

    def test_get_current_condition(self):
        data = accuweather.get_current_condition(LAT_TEST, LONG_TEST)
        assert(data is not None)
        keys = data.keys()
        assert("UVIndex" in keys)
        assert("Visibility" in keys)
        assert("Precip1hr" in keys)

    def test_get_uv_index(self):
        uv_index = accuweather.get_uv_index(LAT_TEST, LONG_TEST)
        assert(uv_index is not None)
        assert(type(uv_index) == int)

    def test_get_visibility_precipitation(self):
        visibility, precipitation = accuweather.get_visibility_precipitation(LAT_TEST, LONG_TEST)
        assert(visibility is not None)
        assert(type(visibility) == float)
        assert(precipitation is not None)
        assert(type(precipitation) == float)
