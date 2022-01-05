"""Functions and imports to initiate Flask app"""

import logging

from apiflask import APIFlask

from .config import get_config

configobj = get_config()

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(configobj.LOGGING_LEVEL)
if configobj.LOGGING_FILE:
    fh = logging.FileHandler(configobj.LOGGING_FILE)
    fh.setLevel(configobj.LOGGING_LEVEL)
    logger.addHandler(fh)

from .controller import register_endpoints


def create_app() -> APIFlask:
    """
    function to initiate the app
    """
    kwargs = {}
    if not configobj.DOCS_URL_ENABLE:
        kwargs.update(dict(docs_path=None, redoc_path=None))
    app = APIFlask(
        __name__, title="Meteo French API", version=configobj.VERSION, **kwargs
    )
    app.config.from_object(configobj)
    register_endpoints(app)
    return app
