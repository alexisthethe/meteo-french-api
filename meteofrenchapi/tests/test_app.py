import unittest
from meteofrenchapi import create_app
from meteofrenchapi.tests import LAT_TEST, LONG_TEST

app = create_app()


class AppTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()
        self.params_latlong_test = {
            "lat": LAT_TEST,
            "long": LONG_TEST,
        }

    def test_index(self) -> None:
        res = self.client.get("/")
        assert(res.status_code == 200)
        data = res.json
        assert("name" in data)
        assert(data["name"] == app.name)
        assert("version" in data)
        assert(data["version"] == app.config['VERSION'])

    def test_get_uv_index(self) -> None:
        res = self.client.get("/uv", query_string=self.params_latlong_test)
        assert(res.status_code == 200)
        data = res.json
        assert("uv_index" in data)
        assert(type(data["uv_index"]) == int)

    def test_get_precipitation(self) -> None:
        res = self.client.get("/precipitation", query_string=self.params_latlong_test)
        assert(res.status_code == 200)
        data = res.json
        assert("visibility" in data)
        assert(type(data["visibility"]) == float)
        assert("precipitation" in data)
        assert(type(data["precipitation"]) == float)
