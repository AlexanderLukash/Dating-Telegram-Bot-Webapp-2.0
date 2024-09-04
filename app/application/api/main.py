from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.api.v1.urls import router as v1_router
from app.bot.main import (
    bot,
    dp,
)
from app.settings.config import load_config


config = load_config("././.env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    url_webhook = config.webhook_url + "/api/v1/webhook"
    await bot.set_webhook(
        url=url_webhook,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    yield
    await bot.delete_webhook()


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
