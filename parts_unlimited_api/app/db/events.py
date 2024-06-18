from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to DB...")

    # echo=True show generated SQL queries in the console
    engine = create_engine(settings.database_url, echo=settings.debug)
    app.state.engine = engine
    app.state.session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    logger.info("Connection established.")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database...")

    app.state.engine.dispose()

    logger.info("Connection closed.")
