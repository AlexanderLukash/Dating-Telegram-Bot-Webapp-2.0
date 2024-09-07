from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    User,
)
from punq import Container

from app.bot.handlers.user.profile import profile
from app.domain.entities.users import UserEntity
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


user_router: Router = Router(
    name="User router",
)


def welcome_message(user: User) -> str:
    message: str = f"""Hello, {user.first_name}!
Welcome to our dating app!
On our platform, you can:
- Find new friends and partners
- Use our convenient filters to match profiles
- Communicate through private messages
- And much more!
If you have any questions or suggestions, feel free to contact our support team.
We wish you an enjoyable experience and good luck in your search!"""
    return message


@user_router.message(CommandStart())
async def start(message: Message, container: Container = init_container()):
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        user = UserEntity.from_telegram_user(user=message.from_user)
        await service.create_user(user)
        await message.answer(welcome_message(user=message.from_user))
    except ApplicationException:
        await profile(message)
