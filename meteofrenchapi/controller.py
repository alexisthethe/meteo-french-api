"""Controllers for endpoints of the API"""

from apiflask import APIFlask, Schema, input, output, abort, doc
from apiflask.fields import Float, Integer, String
from marshmallow.exceptions import ValidationError
from werkzeug.wrappers import Response as FlaskResponse


from meteofrenchapi.core.accuweather import (
    get_visibility_precipitation,
    get_uv_index,
    AwException,
)


# INPUTS SCHEMAS


class GeolocationParams(Schema):
    """
    Schema for Geolocation params
    """

    lat = Float(
        required=True,
        metadata={
            "title": "Latitude",
            "description": "The latitude of the geoposition where to get weather information.",
            "example": 48.870502,
        },
    )
    long = Float(
        required=True,
        metadata={
            "title": "Longitude",
            "description": "The longitude of the geoposition where to get weather information.",
            "example": 2.304897,
        },
    )


# OUTPUT SCHEMAS


class ApiInfoResponse(Schema):
    """
    Schema for index response
    """

    name = String(
        metadata={
            "title": "Name",
            "description": "The name of the API.",
            "example": "apiname",
        }
    )
    version = String(
        metadata={
            "title": "Version",
            "description": "The version of the API.",
            "example": "0.0.1",
        }
    )


class PrecipitationResponse(Schema):
    """
    Schema for precipitation response
    """

    visibility = Float(
        metadata={
            "title": "Visibility",
            "description": "The current visibility in meters.",
            "example": 9700.0,
        }
    )
    precipitation = Float(
        metadata={
            "title": "Precipitation",
            "description": "Amount of precipitation that has fallen in the past hour in meters.",
            "example": 0.001,
        }
    )


class UvResponse(Schema):
    """
    Schema for uv response
    """

    uv_index = Integer(
        metadata={"title": "UvIndex", "description": "UV index", "example": 1}
    )


# ENDPOINTS


def register_endpoints(app: APIFlask) -> None:
    """
    function to register endpoints into the given app
    """

    @app.get("/")
    @doc(tag="Weather", operation_id="getApiInfo")
    @output(ApiInfoResponse, description="Successful response. API info")
    def index() -> FlaskResponse:
        """
        Returns a json containing the generic information about the current API.
        """
        response = ApiInfoResponse().load(
            {
                "name": app.name,
                "version": app.config["VERSION"],
            }
        )
        return response

    @app.get("/precipitation")
    @doc(tag="Weather", operation_id="getPrecipitation")
    @input(GeolocationParams, location="query")
    @output(
        PrecipitationResponse,
        description="Successful response. Precipitation information",
    )
    def get_precipitation(geolocation: GeolocationParams) -> FlaskResponse:
        """
        Returns a json containing the visibility
        and Amount of precipitation for a specific
        location defined with latitude and longitude.
        """
        try:
            visibility, precipitation = get_visibility_precipitation(
                geolocation["lat"], geolocation["long"]
            )
            response = PrecipitationResponse().load(
                {
                    "visibility": visibility,
                    "precipitation": precipitation,
                }
            )
        except (AwException, ValidationError) as err:
            print(err.messages)
            print(err.valid_data)
            abort(500)
        return response

    @app.get("/uv")
    @doc(tag="Weather", operation_id="getUv")
    @input(GeolocationParams, location="query")
    @output(UvResponse, description="Successful response. UV Index information")
    def get_uv(geolocation: GeolocationParams) -> FlaskResponse:
        """
        Return the current UV index for a specific
        location defined with latitude and longitude.
        """
        try:
            uv_index = get_uv_index(geolocation["lat"], geolocation["long"])
            response = UvResponse().load(
                {
                    "uv_index": uv_index,
                }
            )
        except (AwException, ValidationError) as err:
            print(err.messages)
            print(err.valid_data)
            abort(500)
        return response
