from aiogram import Dispatcher

from app.bot.handlers.user.start import user_router as user_start_router


def register_routers(dp: Dispatcher):
    dp.include_router(user_start_router)
