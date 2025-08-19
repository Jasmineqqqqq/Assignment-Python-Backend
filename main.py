"""Application entry point."""

from fastapi import FastAPI

from . import database
from .routers import appointments, auth, status, users


def create_app() -> FastAPI:
    app = FastAPI(
        title="Bharat Teleclinic API",
        description="A simplified telemedicine backend service.",
        version="0.1.1",
    )

    @app.on_event("startup")
    def on_startup() -> None:
        database.init_db()

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(appointments.router)
    app.include_router(status.router)
    return app


app = create_app()