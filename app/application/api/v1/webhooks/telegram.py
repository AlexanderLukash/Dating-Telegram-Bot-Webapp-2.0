from fastapi import APIRouter
from fastapi.requests import Request

from aiogram.types import Update

from app.bot.main import (
    bot,
    dp,
)


router = APIRouter(
    tags=["Telegram"],
)


@router.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
