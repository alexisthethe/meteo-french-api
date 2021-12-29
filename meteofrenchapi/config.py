import os


class ConfigBase(object):
    """Base configuration."""

    # General
    VERSION = '0.1.0'
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    PORT = os.environ.get('PORT', '')
    DOCS_URL_ENABLE = False

    # Environment variables
    ENV = os.getenv('ENV')

    # OpenAPI Documentation
    DESCRIPTION = 'A simple weather API'
    CONTACT = {
        'name': 'API Support',
        'url': 'https://alexisthethe.github.io/',
        'email': 'alexisthethe@gmail.com'
    }
    LICENSE = {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
    TAGS = [
        {'name': 'Weather', 'description': 'Endpoints for weather information requests'},
    ]
    SPEC_FORMAT = 'yaml'
    LOCAL_SPEC_PATH = os.path.join(APP_DIR, "openapi.yaml")

    # Accuweather
    ACCUWEATHER_TOKEN = os.getenv('ACCUWEATHER_TOKEN')
    ACCUWEATHER_URL = os.getenv('ACCUWEATHER_URL')


class ProdConfig(ConfigBase):
    """Production configuration."""

    DEBUG = False


class StagingConfig(ConfigBase):
    """Staging configuration."""

    DEBUG = False


class DevConfig(ConfigBase):
    """Development configuration."""

    DOCS_URL_ENABLE = True
    DEBUG = True


class TestConfig(ConfigBase):
    """Staging configuration."""

    DOCS_URL_ENABLE = True
    TESTING = True
    DEBUG = True


def get_config():
    env_config = {
        "prod": ProdConfig,
        "staging": StagingConfig,
        "dev": DevConfig,
        "test": TestConfig
    }
    env = os.getenv("ENV", "prod")
    return env_config[env]
