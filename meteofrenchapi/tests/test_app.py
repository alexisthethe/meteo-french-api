"""Unit tests for app endpoints"""

import unittest
from meteofrenchapi import create_app
from meteofrenchapi.tests import LT_TEST, LG_TEST

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
        self.params_ltlg_test = {
            "lt": LT_TEST,
            "lg": LG_TEST,
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
        self.assertEqual(data["version"], app.config["VERSION"])

    def test_get_uvidx(self) -> None:
        """
        test endpoint /uvidx
        """
        res = self.client.get("/uvidx", query_string=self.params_ltlg_test)
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertIn("uvidx", data)
        self.assertIsInstance(data["uvidx"], int)

    def test_get_prcpt(self) -> None:
        """
        test endpoint /prcpt
        """
        res = self.client.get("/prcpt", query_string=self.params_ltlg_test)
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertIn("vis", data)
        self.assertIsInstance(data["vis"], float)
        self.assertIn("prcpt", data)
        self.assertIsInstance(data["prcpt"], float)
