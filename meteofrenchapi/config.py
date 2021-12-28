import os




class ConfigBase(object):
    """Base configuration."""

    # General
    VERSION = '0.1.0'
    SECRET_KEY = os.environ.get('SECRET_KEY', '')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    PORT = os.environ.get('PORT', '')

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
    SERVERS = [
        {'name': 'Development Server', 'url': 'http://localhost:{}'.format(PORT)},
        {'name': 'Production Server', 'url': 'http://api.example.com'},
        {'name': 'Testing Server', 'url': 'http://test.example.com'}
    ]
    SPEC_FORMAT = 'yaml'
    LOCAL_SPEC_PATH = os.path.join(APP_DIR, "openapi.yaml")


class ProdConfig(ConfigBase):
    """Production configuration."""

    DEBUG = False


class StagingConfig(ConfigBase):
    """Staging configuration."""

    DEBUG = False


class DevConfig(ConfigBase):
    """Development configuration."""

    DEBUG = True


class TestConfig(ConfigBase):
    """Staging configuration."""

    TESTING = True
    DEBUG = True
