from app.bot.main import (
    bot,
    dp,
)
from app.settings.config import Config
from app.settings.logger import setup_logging


async def set_bot_webhook(config: Config = Config()):
    await bot.set_webhook(
        url=config.full_webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


async def delete_bot_webhook():
    await bot.delete_webhook()


def start_logger():
    setup_logging()
