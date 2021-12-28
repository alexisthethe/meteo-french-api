import os
import requests

from meteofrenchapi import configobj

# Constants
GEOPOSITION_EP = "/locations/v1/cities/geoposition/search"
CURRENTCONDITIONS_EP = "/currentconditions/v1"
DEC_ROUND = 4


def base_get(endpoint, params={}):
    url = configobj.ACCUWEATHER_URL + endpoint
    params["apikey"] = configobj.ACCUWEATHER_TOKEN
    res = requests.get(url, params=params)
    if not res.ok:
        print("ERROR during request to {} (err={}, msg={})".format(url, res.status_code, res.text))
    return res


def get_location_key(lat, long):
    params = {"q": "{},{}".format(lat, long)}
    res = base_get(GEOPOSITION_EP, params)
    location_key = None
    if res.ok:
        location_key = res.json().get("Key")
    else:
        print("ERROR: cannot get locationKey for ({},{})".format(lat, long, res.status_code))
    return location_key


def convert_to_m(valueobj):
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
        print("ERROR: UnitType unknown while converting {} to meters".format(valueobj))
        return None
    value = round(value, DEC_ROUND)
    return value


def get_current_condition(lat, long):
    location_key = get_location_key(lat, long)
    if location_key is None:
        print("ERROR get_uv_index: location_key is None")
        return None
    endpoint = CURRENTCONDITIONS_EP + "/{}".format(location_key)
    params = {"details": True}
    res = base_get(endpoint, params)
    if not res.ok:
        print("ERROR get_current_condition: request failed ({})".format(res.status_code))
        return None
    data = res.json()
    if not len(data):
        print("ERROR get_current_condition: data is empty")
        return None
    return data[0]


def get_uv_index(lat, long):
    data = get_current_condition(lat, long)
    if data is None:
        return None
    return data.get('UVIndex')


def get_visibility_precipitation(lat, long):
    data = get_current_condition(lat, long)
    if data is None:
        return None
    visibility = data.get('Visibility')
    if visibility is not None: visibility = convert_to_m(visibility)
    precipitation = data.get('Precip1hr')
    if precipitation is not None: precipitation = convert_to_m(precipitation)
    return (visibility, precipitation)
