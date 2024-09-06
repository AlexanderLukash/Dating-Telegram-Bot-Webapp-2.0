from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    User,
)
from punq import Container

from app.domain.entities.users import UserEntity
from app.domain.values.users import Name
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


user_router: Router = Router(
    name="User router",
)


def welcome_message(user: User) -> str:
    message: str = (
        f"Hello, {user.first_name}!\n"
        "Welcome to our dating app!\n\n"
        "On our platform, you can:\n"
        "- Find new friends and partners\n"
        "- Use our convenient filters to match profiles\n"
        "- Communicate through private messages\n"
        "- And much more!\n\n"
        "If you have any questions or suggestions, feel free to contact our support team.\n"
        "We wish you an enjoyable experience and good luck in your search!\n"
    )
    return message


@user_router.message(CommandStart())
async def start(message: Message, container: Container = init_container()):
    service: BaseUsersService = container.resolve(BaseUsersService)
    telegram_id = message.from_user.id
    username = message.from_user.username or ""
    name = Name(message.from_user.first_name)

    user_entity = UserEntity(
        telegram_id=telegram_id,
        username=username,
        name=name,
    )

    await service.create_user(user_entity)
    await message.answer(welcome_message(user=message.from_user))
