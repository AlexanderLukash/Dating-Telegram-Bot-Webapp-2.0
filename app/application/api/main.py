from fastapi import FastAPI

from app.application.api.v1.urls import router as v1_router


def create_app():
    app = FastAPI(
        title="Dating Telegram Bot API",
        description="API for creating, updating, and deleting dating profiles",
        version="1.0.0",
        docs_url="/api/docs",
        debug=True,
    )
    app.include_router(v1_router, prefix="/api")
    return app
