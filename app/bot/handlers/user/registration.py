from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from punq import Container

from app.bot.keyboards.reply import (
    remove_keyboard,
    user_name_keyboard,
)
from app.bot.utils.states import UserForm
from app.domain.exceptions.base import ApplicationException
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


registration_router = Router(
    name="Registration router",
)


@registration_router.message(UserForm.name)
async def user_set_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserForm.age)

    await message.answer(
        text="How old are you?",
        reply_markup=remove_keyboard,
    )


@registration_router.message(Command("form"))
async def registration_form(
    message: Message,
    state: FSMContext,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)

    try:
        await service.get_user(telegram_id=message.from_user.id)

        if not message.from_user.username:
            await message.answer(
                text="First, set the <b><i>username</i></b> in the settings of your Telegram account."
                "\nAnd then use the /form command again",
            )

        await state.set_state(UserForm.name)
        await message.answer(
            text="Let's get started, enter your name.",
            reply_markup=user_name_keyboard(message.from_user.first_name),
        )

    except ApplicationException:
        await message.answer(text="First, enter the command: <b>/start</b>")
