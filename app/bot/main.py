from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from punq import Container

from app.bot.callbacks.setup import register_callback_routers
from app.bot.handlers.setup import register_routers
from app.logic.init import init_container
from app.settings.config import Config


container: Container = init_container()
config: Config = container.resolve(Config)

bot = Bot(
    token=config.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
register_routers(dp)
register_callback_routers(dp)
