"""Logic functions for to get Accuweather data"""

from json.decoder import JSONDecodeError
from typing import Tuple

import requests

from meteofrenchapi import configobj


# Constants
GEOPOSITION_EP = "/locations/v1/cities/geoposition/search"
CURRENTCONDITIONS_EP = "/currentconditions/v1"
DEC_ROUND = 4


# Exceptions
class AwException(Exception):
    """
    Base class for Accuweather exceptions
    """


class AwRequestError(AwException):
    """
    Exception when error a request to Accuweather API failed
    """

    def __init__(self, url, res):
        super().__init__(
            f"request failure {url} (err={res.status_code}, msg={res.text})"
        )


# Functions


def base_get(endpoint: str, params: dict = None) -> requests.Response:
    """
    Base function for calls to Accuweather API
    """
    if params is None:
        params = {}
    url = configobj.ACCUWEATHER_URL + endpoint
    params["apikey"] = configobj.ACCUWEATHER_TOKEN
    res = requests.get(url, params=params)
    if not res.ok:
        raise AwRequestError(url, res)
    return res


def get_json(res: requests.Response) -> dict:
    """
    Base function to get JSON data from Accuweather response or raise AwException
    """
    try:
        return res.json()
    except JSONDecodeError as err:
        raise AwException(
            f"could not get JSON from Accuweather response {res.text}"
        ) from err


def get_data(data: dict, key: str):
    """
    Base function to get value from data from key or raise AwException
    """
    try:
        return data[key]
    except KeyError as err:
        raise AwException(f"{key} not found") from err


def get_location_key(lat: float, long: float) -> str:
    """
    Retrieve locationKey with Accuweather API
    """
    params = {"q": f"{lat},{long}"}
    res = base_get(GEOPOSITION_EP, params)
    data = get_json(res)
    return get_data(data, "Key")


def convert_to_m(valueobj: dict) -> float:
    """
    Function to convert value object got from Accuweather in meter
    """
    valueobj_m = valueobj.get("Metric")
    unit_type = valueobj_m.get("UnitType")
    value = valueobj_m["Value"]
    # mm
    if unit_type == 3:
        value *= 0.001
    # cm
    elif unit_type == 4:
        value *= 0.01
    # m
    elif unit_type == 5:
        pass
    # km
    elif unit_type == 6:
        value *= 1000
    else:
        raise AwException(f"UnitType unknown while converting {valueobj} to meters")
    value = round(value, DEC_ROUND)
    return value


def get_current_condition(lat: float, long: float) -> dict:
    """
    Retrieve current conditions data according to latitude and longitude
    """
    location_key = get_location_key(lat, long)
    endpoint = CURRENTCONDITIONS_EP + f"/{location_key}"
    params = {"details": True}
    res = base_get(endpoint, params)
    data = get_json(res)
    if not data:
        raise AwException("data current_condition is empty")
    return data[0]


def get_uv_index(lat: float, long: float) -> int:
    """
    get UV index at geoposition (lat, long) from Accuweather API
    """
    data = get_current_condition(lat, long)
    return get_data(data, "UVIndex")


def get_visibility_precipitation(lat: float, long: float) -> Tuple[float, float]:
    """
    get visibility and precipitation in meters at geoposition (lat, long) from Accuweather API
    """
    data = get_current_condition(lat, long)
    visibility = get_data(data, "Visibility")
    precipitation = get_data(data, "Precip1hr")
    visibility = convert_to_m(visibility)
    precipitation = convert_to_m(precipitation)
    return (visibility, precipitation)
