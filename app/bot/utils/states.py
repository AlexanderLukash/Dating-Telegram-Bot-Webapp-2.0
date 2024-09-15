from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class UserForm(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    looking_for = State()
    about = State()


class UserAboutUpdate(StatesGroup):
    about = State()
