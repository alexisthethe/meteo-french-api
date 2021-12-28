import os
from apiflask import APIFlask

from .config import get_config
configobj = get_config()
from .controller import register_endpoints




def create_app():
    app = APIFlask(__name__, title='Meteo French API', version=configobj.VERSION)
    app.config.from_object(configobj)
    register_endpoints(app)
    return app
