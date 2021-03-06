"""Configs"""

import os
from dataclasses import dataclass


@dataclass
class ConfigBase:
    """Base configuration."""

    # General
    VERSION = "0.1.0"
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    PORT = os.environ.get("PORT", "")
    DOCS_URL_ENABLE = False

    # Environment variables
    ENV = os.getenv("ENV")

    # OpenAPI Documentation
    DESCRIPTION = "A simple weather API"
    CONTACT = {
        "name": "API Support",
        "url": "https://alexisthethe.github.io/",
        "email": "alexisthethe@gmail.com",
    }
    LICENSE = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
    TAGS = [
        {
            "name": "Weather",
            "description": "Endpoints for weather information requests",
        },
    ]
    SPEC_FORMAT = "yaml"
    LOCAL_SPEC_PATH = os.path.join(APP_DIR, "openapi.yaml")

    # Logging
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "WARNING")
    LOGGING_FILE = os.getenv("LOGGING_FILE", None)

    # ACCWEA
    ACCWEA_TOKEN = os.getenv("ACCWEA_TOKEN")
    ACCWEA_URL = os.getenv("ACCWEA_URL")
    VIS_KEY = os.getenv("VIS_KEY")
    PRCPT_KEY = os.getenv("PRCPT_KEY")
    UVIDX_KEY = os.getenv("UVIDX_KEY")


@dataclass
class ProdConfig(ConfigBase):
    """Production configuration."""

    DEBUG = False


@dataclass
class StagingConfig(ConfigBase):
    """Staging configuration."""

    DEBUG = False


@dataclass
class DevConfig(ConfigBase):
    """Development configuration."""

    DOCS_URL_ENABLE = True
    DEBUG = True


@dataclass
class TestConfig(ConfigBase):
    """Staging configuration."""

    DOCS_URL_ENABLE = True
    TESTING = True
    DEBUG = True


def get_config() -> ConfigBase:
    """
    Get config object from environment variable ENV
    """
    env_config = {
        "prod": ProdConfig,
        "staging": StagingConfig,
        "dev": DevConfig,
        "test": TestConfig,
    }
    env = os.getenv("ENV", "prod")
    return env_config[env]
