from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from punq import Container

from app.bot.handlers.users.profile import profile
from app.bot.utils.constants import (
    first_welcome_message,
    second_welcome_message,
)
from app.domain.entities.users import UserEntity
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


user_router: Router = Router(
    name="User router",
)


@user_router.message(CommandStart())
async def start(message: Message, container: Container = init_container()):
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        user = UserEntity.from_telegram_user(user=message.from_user)
        await service.create_user(user)
        await message.answer(first_welcome_message(user=message.from_user))
    except ApplicationException:
        if await service.check_user_is_active(telegram_id=message.from_user.id):
            await profile(message)
        else:
            await message.answer(second_welcome_message(user=message.from_user))
