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
from app.bot.utils.constants import profile_text_message
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

    if isinstance(update, Message):
        user = await service.get_user(telegram_id=update.from_user.id)
        await update.answer_photo(
            photo=user.photo,
            caption=profile_text_message(user=user),
            reply_markup=profile_inline_kb(user_id=update.from_user.id, liked_by=False),
        )
    else:
        user = await service.get_user(telegram_id=update.from_user.id)
        await update.message.edit_text(
            text=profile_text_message(user=user),
            reply_markup=profile_inline_kb(user_id=update.from_user.id, liked_by=False),
        )
