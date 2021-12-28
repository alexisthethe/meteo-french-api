from apiflask import Schema, input, output, abort, doc
from apiflask.fields import Float, Integer
from marshmallow.exceptions import ValidationError


# INPUTS SCHEMAS

class GeolocationParams(Schema):
    lat = Float(
        required=True,
        metadata={
            'title': 'Latitude',
            'description': 'The latitude of the geoposition where to get weather information.',
            'example': 48.870502
        }
    )
    long = Float(
        required=True,
        metadata={
            'title': 'Longitude',
            'description': 'The longitude of the geoposition where to get weather information.',
            'example': 2.304897
        }
    )


# OUTPUT SCHEMAS

class PrecipitationResponse(Schema):
    visibility = Float(
        metadata={
            'title': 'Visibility',
            'description': 'The current visibility in meters.',
            'example': 9700.0
        }
    )
    precipitation = Float(
        metadata={
            'title': 'Precipitation',
            'description': 'Amount of precipitation that has fallen in the past hour in meters.',
            'example': 0.001
        }
    )

class UvResponse(Schema):
    uv_index = Integer(
        metadata={
            'title': 'UvIndex',
            'description': 'UV index',
            'example': 1
        }
    )


# ENDPOINTS

def register_endpoints(app):

    @app.get('/precipitation')
    @doc(tag='Weather', operation_id='getPrecipitation')
    @input(GeolocationParams, location='query')
    @output(PrecipitationResponse, description='Successful response. Precipitation information')
    def get_precipitation(geolocation):
        """
        Returns a json containing the visibility
        and Amount of precipitation for a specific
        location defined with latitude and longitude.
        """
        print(geolocation)
        try:
            response = PrecipitationResponse().load({
                'precipitation': geolocation['lat'],
                'visibility': geolocation['long']
            })
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)
            abort(500)
        return response

    @app.get('/uv')
    @doc(tag='Weather', operation_id='getUv')
    @input(GeolocationParams, location='query')
    @output(UvResponse, description='Successful response. UV Index information')
    def get_uv(geolocation):
        """
        Return the current UV index for a specific
        location defined with latitude and longitude.
        """
        response = UvResponse().load({
            'uv_index': 1,
        })
        return response
