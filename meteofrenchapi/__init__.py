import os
from apiflask import APIFlask

from .config import ProdConfig, StagingConfig, DevConfig, TestConfig
from .controller import register_endpoints


def create_app():
    configobj = get_config()
    app = APIFlask(__name__, title='Meteo French API', version=configobj.VERSION)
    app.config.from_object(configobj)
    register_endpoints(app)
    return app


def get_config():
    env_config = {
        "prod": ProdConfig,
        "staging": StagingConfig,
        "dev": DevConfig,
        "test": TestConfig
    }
    env = os.getenv("ENV", "prod")
    return env_config[env]
