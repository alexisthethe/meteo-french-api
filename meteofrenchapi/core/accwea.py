"""Logic functions for to get ACCWEA data"""

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
    Base class for ACCWEA exceptions
    """


class AwRequestError(AwException):
    """
    Exception when error a request to ACCWEA API failed
    """

    def __init__(self, url, params, res):
        super().__init__(
            f"request failure {url} ({params}) (err={res.status_code}, msg={res.text})"
        )


# Functions


def base_get(endpoint: str, params: dict = None) -> requests.Response:
    """
    Base function for calls to ACCWEA API
    """
    if params is None:
        params = {}
    url = configobj.ACCWEA_URL + endpoint
    params["apikey"] = configobj.ACCWEA_TOKEN
    res = requests.get(url, params=params)
    if not res.ok:
        raise AwRequestError(url, params, res)
    return res


def get_json(res: requests.Response) -> dict:
    """
    Base function to get JSON data from ACCWEA response or raise AwException
    """
    try:
        return res.json()
    except JSONDecodeError as err:
        raise AwException(
            f"could not get JSON from ACCWEA response {res.text}"
        ) from err


def get_data(data: dict, key: str):
    """
    Base function to get value from data from key or raise AwException
    """
    try:
        return data[key]
    except KeyError as err:
        raise AwException(f"{key} not found") from err


def get_location_key(lt: float, lg: float) -> str:
    """
    Retrieve locationKey with ACCWEA API
    """
    params = {"q": f"{lt},{lg}"}
    res = base_get(GEOPOSITION_EP, params)
    data = get_json(res)
    return get_data(data, "Key")


def convert_to_m(valueobj: dict) -> float:
    """
    Function to convert value object got from ACCWEA in meter
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


def get_current_condition(lt: float, lg: float) -> dict:
    """
    Retrieve current conditions data according to lt and lg
    """
    location_key = get_location_key(lt, lg)
    endpoint = CURRENTCONDITIONS_EP + f"/{location_key}"
    params = {"details": True}
    res = base_get(endpoint, params)
    data = get_json(res)
    if not data:
        raise AwException("data current_condition is empty")
    return data[0]


def get_uvidx(lt: float, lg: float) -> int:
    """
    get uvidx at geoposition (lt, lg) from ACCWEA API
    """
    data = get_current_condition(lt, lg)
    return get_data(data, configobj.UVIDX_KEY)


def get_vis_prcpt(lt: float, lg: float) -> Tuple[float, float]:
    """
    get vis and prcpt in meters at geoposition (lt, lg) from ACCWEA API
    """
    data = get_current_condition(lt, lg)
    vis = get_data(data, configobj.VIS_KEY)
    prcpt = get_data(data, configobj.PRCPT_KEY)
    vis = convert_to_m(vis)
    prcpt = convert_to_m(prcpt)
    return (vis, prcpt)
