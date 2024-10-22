import logging

from punq import Container

from app.bot.main import bot
from app.bot.utils.constants import profile_text_message
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


async def send_liked_message(
    from_user_id: int,
    to_user_id: int,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        user = await service.get_user(telegram_id=from_user_id)

        await bot.send_photo(
            to_user_id,
            photo=user.photo,
            caption=f"<b>You were liked 💗</b>\n{profile_text_message(user=user)}",
        )
    except Exception as e:
        error_message = f"Failed to send message: {e}"
        logging.error({"error_message": error_message})
