from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.keyboards.inline import (
    about_confirm_keyboard,
    profile_edit_keyboard,
)
from app.bot.keyboards.reply import about_skip_keyboard
from app.bot.utils.states import UserAboutUpdate


callback_profile_router = Router()


@callback_profile_router.callback_query(F.data == "profile_edit")
async def profile_edit(callback: CallbackQuery):
    # Send a new message with profile edit options and the respective keyboard
    await callback.message.edit_text(
        text="1. Cancel.\n"
        "2. Fill out the profile again.\n"
        "3. Change photo.\n"
        "4. Change the text of the profile.\n",
        reply_markup=profile_edit_keyboard(),
    )


@callback_profile_router.callback_query(F.data == "about_edit")
async def about_edit(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Are you sure you want to change your about section?",
        reply_markup=about_confirm_keyboard(),
    )


@callback_profile_router.callback_query(F.data == "about_confirm")
async def about_edit_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Delete the confirmation message
    await state.set_state(
        UserAboutUpdate.about,
    )  # Set the state to AboutEditState.about
    # Send a message to prompt the user to input something about themselves or skip
    await callback.message.answer(
        text="Tell us something about yourself that might interest someone, "
        "or click the button to leave this field blank.",
        reply_markup=about_skip_keyboard,  # Provide a keyboard to skip the about section
    )
