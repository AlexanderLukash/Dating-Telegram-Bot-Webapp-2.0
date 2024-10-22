import time

from aiogram import (
    F,
    Router,
)
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
)
from punq import Container

from app.bot.keyboards.inline import profile_inline_kb
from app.bot.utils.constants import user_profile_text_message
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


user_profile_router: Router = Router(
    name="User profile router",
)


@user_profile_router.message(Command("profile"))
@user_profile_router.callback_query(F.data == "profile_page")
async def profile(
    update: Message | CallbackQuery,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)

    user = await service.get_user(telegram_id=update.from_user.id)

    if isinstance(update, Message):
        await update.answer_photo(
            photo=f"{user.photo}?nocache={int(time.time())}",
            caption=user_profile_text_message(user=user),
            reply_markup=profile_inline_kb(user_id=update.from_user.id, liked_by=False),
        )
    else:
        await update.message.delete()
        await update.message.answer_photo(
            photo=f"{user.photo}?nocache={int(time.time())}",
            caption=user_profile_text_message(user=user),
            reply_markup=profile_inline_kb(user_id=update.from_user.id, liked_by=False),
        )
