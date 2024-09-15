from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.callbacks.setup import register_callback_routers
from app.bot.handlers.setup import register_routers
from app.settings.config import Config


config: Config = Config()

bot = Bot(
    token=config.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
register_routers(dp)
register_callback_routers(dp)
