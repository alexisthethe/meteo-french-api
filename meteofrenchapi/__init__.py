"""Functions and imports to initiate Flask app"""

from apiflask import APIFlask

from .config import get_config

configobj = get_config()
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
