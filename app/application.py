"""
Application entrypoint (FastAPI)


@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""

from fastapi import FastAPI

from . import endpoints
from .containers import Container


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    application = FastAPI()
    application.container = container
    application.include_router(endpoints.router)

    return application


app = create_app()
