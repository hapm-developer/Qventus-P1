import logging

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    """
    Development Application settings class.
    """

    debug: bool = True

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".test.env"
