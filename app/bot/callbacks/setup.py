from aiogram import Dispatcher

from app.bot.callbacks.users.likes import callback_like_router
from app.bot.callbacks.users.profile_edit import callback_profile_router


def register_callback_routers(dp: Dispatcher):
    dp.include_router(callback_profile_router)
    dp.include_router(callback_like_router)
