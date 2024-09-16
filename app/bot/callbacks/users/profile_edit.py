from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.keyboards.inline import (
    about_confirm_keyboard,
    profile_edit_keyboard,
    re_registration_confirm_keyboard,
)
from app.bot.keyboards.reply import (
    about_skip_keyboard,
    user_name_keyboard,
)
from app.bot.utils.states import (
    UserAboutUpdate,
    UserForm,
)


callback_profile_router = Router()


@callback_profile_router.callback_query(F.data == "profile_edit")
async def profile_edit(callback: CallbackQuery):
    await callback.message.edit_text(
        text="1. Cancel.\n"
        "2. Fill out the profile again.\n"
        "3. Change photo.\n"
        "4. Change the text of the profile.\n",
        reply_markup=profile_edit_keyboard(),
    )


@callback_profile_router.callback_query(F.data == "form")
async def re_registration_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Are you sure you want to fill out your profile again?",
        reply_markup=re_registration_confirm_keyboard(),
    )


@callback_profile_router.callback_query(F.data == "form_confirm")
async def form_edit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserForm.name)
    await callback.message.delete()
    await callback.message.answer(
        text="Let's get started, enter your name.",
        reply_markup=user_name_keyboard(callback.from_user.first_name),
    )


@callback_profile_router.callback_query(F.data == "about_edit")
async def about_edit(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Are you sure you want to change your about section?",
        reply_markup=about_confirm_keyboard(),
    )


@callback_profile_router.callback_query(F.data == "about_confirm")
async def about_edit_confirm(callback: CallbackQuery, state: FSMContext):
    await state.set_state(
        UserAboutUpdate.about,
    )

    await callback.message.edit_text(
        text="Tell us something about yourself that might interest someone, "
        "or click the button to leave this field blank.",
        reply_markup=about_skip_keyboard,
    )
