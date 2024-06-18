from typing import Callable

from app.core.settings.app import AppSettings
from app.db.events import close_db_connection, connect_to_db
from fastapi import FastAPI
from loguru import logger


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:
    """
    Call to init anything you need before start the app.
    """

    async def start_app() -> None:
        await connect_to_db(app, settings)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    Call to shut down anything you need before stop the app.
    """

    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app
