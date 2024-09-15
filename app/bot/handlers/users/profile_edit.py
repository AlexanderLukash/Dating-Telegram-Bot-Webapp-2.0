from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Update
from punq import Container

from app.bot.handlers.users.profile import profile
from app.bot.keyboards.reply import remove_keyboard
from app.bot.utils.states import UserAboutUpdate
from app.domain.exceptions.base import ApplicationException
from app.domain.values.users import AboutText
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


profile_edit_router = Router()


@profile_edit_router.message(UserAboutUpdate.about)
async def about_edit_state(
    message: Update,
    state: FSMContext,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)
    try:
        if message.text.lower() == "🪪 skip":
            about = AboutText(None)
        else:
            about = AboutText(message.text)
        await state.clear()
        await message.answer(
            "You have successfully updated your details.",
            reply_markup=remove_keyboard,
        )

        await service.update_user_about_info(
            telegram_id=message.from_user.id,
            about=about,
        )

        await profile(message)
    except ApplicationException as exception:
        await message.answer(text=exception.message)
