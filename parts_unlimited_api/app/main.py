from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.settings.app import AppSettings
from app.routers.parts import part_router


def create_application() -> FastAPI:
    """
    Creates and initializes FastAPI application.
    """
    settings = AppSettings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    # Include routers
    application.include_router(part_router, prefix=settings.api_v1_prefix)

    # Configure middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Event handlers for startup and shutdown
    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )
    return application


app = create_application()

@app.get("/")
def read_root():
    return {"message": "Welcome to Parts Unlimited API"}
