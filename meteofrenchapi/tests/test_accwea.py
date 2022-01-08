"""Unit tests for accwea.py functions"""

import unittest

from meteofrenchapi.core import accwea
from meteofrenchapi.tests import LT_TEST, LG_TEST


class TestAccwea(unittest.TestCase):
    """
    Unit tests for accwea functions
    """

    def test_base_get(self) -> None:
        """
        test base_get function
        """
        test_endpoint = "/locations/v1/regions"
        res = accwea.base_get(test_endpoint)
        self.assertTrue(res.ok)
        params = {"language": "fr-fr"}
        res = accwea.base_get(test_endpoint, params)
        self.assertTrue(res.ok)

    def test_get_location_key(self) -> None:
        """
        test get_location_key function
        """
        location_key = accwea.get_location_key(LT_TEST, LG_TEST)
        self.assertEqual(location_key, "2608429")

    def test_convert_to_m(self) -> None:
        """
        test convert_to_m function
        """
        # test convertion from mm
        valueobj = {
            "Metric": {"Value": 2.1, "Unit": "mm", "UnitType": 3},
            "Imperial": {"Value": 0.0, "Unit": "in", "UnitType": 1},
        }
        value = accwea.convert_to_m(valueobj)
        self.assertEqual(value, 0.0021)
        # test convertion from cm
        valueobj = {
            "Metric": {"Value": 2.1, "Unit": "cm", "UnitType": 4},
            "Imperial": {"Value": 0.0, "Unit": "in", "UnitType": 1},
        }
        value = accwea.convert_to_m(valueobj)
        self.assertEqual(value, 0.021)
        # test convertion from m
        valueobj = {
            "Metric": {"Value": 2.1, "Unit": "m", "UnitType": 5},
            "Imperial": {"Value": 0.0, "Unit": "in", "UnitType": 1},
        }
        value = accwea.convert_to_m(valueobj)
        self.assertEqual(value, 2.1)
        # test convertion from km
        valueobj = {
            "Metric": {"Value": 2.1, "Unit": "km", "UnitType": 6},
            "Imperial": {"Value": 0.0, "Unit": "in", "UnitType": 1},
        }
        value = accwea.convert_to_m(valueobj)
        self.assertEqual(value, 2100)

    def test_get_current_condition(self) -> None:
        """
        test get_current_condition function
        """
        data = accwea.get_current_condition(LT_TEST, LG_TEST)
        self.assertIsInstance(data, dict)

    def test_get_uvidx(self) -> None:
        """
        test get_uvidx function
        """
        uvidx = accwea.get_uvidx(LT_TEST, LG_TEST)
        self.assertIsInstance(uvidx, int)

    def test_get_vis_prcpt(self) -> None:
        """
        test get_vis_prcpt function
        """
        vis, prcpt = accwea.get_vis_prcpt(LT_TEST, LG_TEST)
        self.assertIsInstance(vis, float)
        self.assertIsInstance(prcpt, float)
