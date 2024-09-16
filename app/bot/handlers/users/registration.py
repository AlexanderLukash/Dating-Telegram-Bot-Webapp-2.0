from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from punq import Container

from app.bot.keyboards.reply import (
    about_skip_keyboard,
    gender_select_keyboard,
    remove_keyboard,
    user_name_keyboard,
)
from app.bot.utils.constants import profile_text_message
from app.bot.utils.states import UserForm
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


registration_router = Router(
    name="Registration router",
)


async def gender_check(message):
    # Check the gender selected by the users
    if message.text.lower() == "👨 man":
        gender = "Man"
        return gender
    elif message.text.lower() == "👧 female":
        gender = "Female"
        return gender
    else:
        await message.answer(
            text="Click on the button 👇",
            reply_markup=gender_select_keyboard,
        )
        return None


@registration_router.message(UserForm.name)
async def user_set_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserForm.age)

    await message.answer(
        text="How old are you?",
        reply_markup=remove_keyboard,
    )


@registration_router.message(UserForm.age)
async def user_set_gender(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(UserForm.gender)
        await message.answer(
            text="What gender are you?",
            reply_markup=gender_select_keyboard,
        )
    else:
        await message.answer(text="Enter the number again!")


@registration_router.message(UserForm.gender)
async def user_set_city(message: Message, state: FSMContext):
    gender = await gender_check(message)

    if gender is not None:
        await state.update_data(gender=gender)
        await state.set_state(UserForm.city)
        await message.answer(
            text="What city are you from?",
            reply_markup=remove_keyboard,
        )


@registration_router.message(UserForm.city)
async def user_set_looking_for(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(text="Enter the correct data.")
    else:
        await state.update_data(city=message.text)
        await state.set_state(UserForm.looking_for)
        await message.answer(
            text="Who do you want to find?",
            reply_markup=gender_select_keyboard,
        )


@registration_router.message(UserForm.looking_for)
async def user_set_about(message: Message, state: FSMContext):
    gender = await gender_check(message)

    if gender is not None:
        await state.update_data(looking_for=gender)
        await state.set_state(UserForm.about)
        await message.answer(
            text="Tell us a little about yourself. (Or click the button below to skip)",
            reply_markup=about_skip_keyboard,
        )


@registration_router.message(UserForm.about)
async def user_set_photo(
    message: Message,
    state: FSMContext,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)

    if message.text.lower() == "🪪 skip":
        await state.update_data(about=None)
    else:
        await state.update_data(about=message.text)

    await message.answer(
        text="Registration is successful.",
        reply_markup=remove_keyboard,
    )

    data = await state.get_data()
    data["is_active"] = True

    await service.update_user_info_after_reg(
        telegram_id=message.from_user.id,
        data=data,
    )

    user = await service.get_user(telegram_id=message.from_user.id)
    await state.clear()
    await message.answer(text=profile_text_message(user=user))


@registration_router.message(Command("form"))
async def registration_form(
    message: Message,
    state: FSMContext,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        user = await service.get_user(telegram_id=message.from_user.id)

        if user.is_active:
            await message.answer(
                text="You are already registered.",
                reply_markup=remove_keyboard,
            )
            await message.answer(text=profile_text_message(user=user))

        elif not message.from_user.username:
            await message.answer(
                text="First, set the <b><i>username</i></b> in the settings of your Telegram account."
                "\nAnd then use the /form command again",
            )

        else:
            await state.set_state(UserForm.name)
            await message.answer(
                text="Let's get started, enter your name.",
                reply_markup=user_name_keyboard(message.from_user.first_name),
            )

    except ApplicationException:
        await message.answer(text="First, enter the command: <b>/start</b>")
