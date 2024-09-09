from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.api.lifespan import (
    delete_bot_webhook,
    set_bot_webhook,
    start_logger,
)
from app.application.api.v1.urls import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_logger()
    await set_bot_webhook()

    yield
    await delete_bot_webhook()


def create_app():
    app = FastAPI(
        title="Dating Telegram Bot API",
        description="API for creating, updating, and deleting dating profiles",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        debug=True,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(v1_router, prefix="/api")

    return app
