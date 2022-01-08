"""Controllers for endpoints of the API"""

from apiflask import APIFlask, Schema, input, output, abort, doc
from apiflask.fields import Float, Integer, String
from marshmallow.exceptions import ValidationError
from werkzeug.wrappers import Response as FlaskResponse


from meteofrenchapi.core.accwea import (
    get_vis_prcpt,
    get_uvidx,
    AwException,
)
from meteofrenchapi import logger


# INPUTS SCHEMAS


class GeolocationParams(Schema):
    """
    Schema for Geolocation params
    """

    lt = Float(
        required=True,
        metadata={
            "title": "Lt",
            "description": "The lt of the geoposition where to get weather information.",
            "example": 48.870502,
        },
    )
    lg = Float(
        required=True,
        metadata={
            "title": "Lg",
            "description": "The lg of the geoposition where to get weather information.",
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


class PrcptResponse(Schema):
    """
    Schema for prcpt response
    """

    vis = Float(
        metadata={
            "title": "Vis",
            "description": "The current vis in meters.",
            "example": 9700.0,
        }
    )
    prcpt = Float(
        metadata={
            "title": "Prcpt",
            "description": "Amount of prcpt that has fallen in the past hour in meters.",
            "example": 0.001,
        }
    )


class UvResponse(Schema):
    """
    Schema for uv response
    """

    uvidx = Integer(metadata={"title": "Uvidx", "description": "uvidx", "example": 1})


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

    @app.get("/prcpt")
    @doc(tag="Weather", operation_id="getPrcpt")
    @input(GeolocationParams, location="query")
    @output(
        PrcptResponse,
        description="Successful response. Prcpt information",
    )
    def get_prcpt(geolocation: GeolocationParams) -> FlaskResponse:
        """
        Returns a json containing the vis
        and Amount of prcpt for a specific
        location defined with lt and lg.
        """
        try:
            vis, prcpt = get_vis_prcpt(geolocation["lt"], geolocation["lg"])
            response = PrcptResponse().load(
                {
                    "vis": vis,
                    "prcpt": prcpt,
                }
            )
        except (AwException, ValidationError):
            abort(500)
        return response

    @app.get("/uvidx")
    @doc(tag="Weather", operation_id="getUv")
    @input(GeolocationParams, location="query")
    @output(UvResponse, description="Successful response. uvidx information")
    def get_uv(geolocation: GeolocationParams) -> FlaskResponse:
        """
        Return the current uvidx for a specific
        location defined with lt and lg.
        """
        try:
            uvidx = get_uvidx(geolocation["lt"], geolocation["lg"])
            response = UvResponse().load(
                {
                    "uvidx": uvidx,
                }
            )
        except (AwException, ValidationError):
            abort(500)
        return response
