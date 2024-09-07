from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    User,
)


user_profile_router: Router = Router(
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


@user_profile_router.message(Command("profile"))
async def profile(message: Message):
    await message.answer("Profile")
