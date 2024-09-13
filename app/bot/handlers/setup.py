from aiogram import Dispatcher

from app.bot.handlers.users.profile import user_profile_router
from app.bot.handlers.users.registration import registration_router
from app.bot.handlers.users.start import user_router as user_start_router


def register_routers(dp: Dispatcher):
    dp.include_router(registration_router)
    dp.include_router(user_profile_router)
    dp.include_router(user_start_router)
