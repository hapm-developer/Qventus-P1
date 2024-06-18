import logging
import sys
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from app.core.logging import InterceptHandler
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Base Application settings class.
    """

    debug: Optional[bool] = True
    api_v1_prefix: str = "/api/v1"
    title: str = "Parts API"
    version: str = "0.0.1"

    allowed_hosts: List[str] = ["*"]

    # Swagger-related parameters
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    swagger_ui_parameters: Dict[str, int] = {"defaultModelsExpandDepth": -1}
    
    # Sqlite
    database_url: str = "sqlite:///./app/db/parts.db"

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True
        env_nested_delimiter = "__"

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """
        FastAPI related arguments.
        """
        return {
            "debug": self.debug,
            "root_path": "",
            "title": self.title,
            "version": self.version,
            "swagger_ui_parameters": self.swagger_ui_parameters
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
