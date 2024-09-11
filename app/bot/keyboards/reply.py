from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def user_name_keyboard(text: str | list) -> ReplyKeyboardMarkup:
    if isinstance(text, str):
        text = [text]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=txt) for txt in text],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


remove_keyboard = ReplyKeyboardRemove()
