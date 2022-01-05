"""Unit tests for app endpoints"""

import unittest
from meteofrenchapi import create_app
from meteofrenchapi.tests import LAT_TEST, LONG_TEST

app = create_app()


class AppTestCase(unittest.TestCase):
    """
    Unit tests for Flask app endpoints
    """

    def setUp(self) -> None:
        """
        set up app tester client and test params
        """
        self.client = app.test_client()
        self.params_latlong_test = {
            "lat": LAT_TEST,
            "long": LONG_TEST,
        }

    def test_index(self) -> None:
        """
        test enpoint /
        """
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertIn("name", data)
        self.assertEqual(data["name"], app.name)
        self.assertIn("version", data)
        self.assertEqual(data["version"], app.config['VERSION'])

    def test_get_uv_index(self) -> None:
        """
        test endpoint /uv
        """
        res = self.client.get("/uv", query_string=self.params_latlong_test)
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertIn("uv_index", data)
        self.assertIsInstance(data["uv_index"], int)

    def test_get_precipitation(self) -> None:
        """
        test endpoint /precipitation
        """
        res = self.client.get("/precipitation", query_string=self.params_latlong_test)
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertIn("visibility", data)
        self.assertIsInstance(data["visibility"], float)
        self.assertIn("precipitation", data)
        self.assertIsInstance(data["precipitation"], float)
