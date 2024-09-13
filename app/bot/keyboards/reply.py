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


gender_select_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="👨 Man",
            ),
            KeyboardButton(
                text="👧 Female",
            ),
        ],
    ],
    resize_keyboard=True,  # Allows the keyboard to resize dynamically
    input_field_placeholder="👇 Press the buttons",  # Placeholder text displayed in the input field
    selective=True,  # Ensures the keyboard is shown only to the specific users who triggered it
)

about_skip_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🪪 Skip",
            ),
        ],
    ],
    resize_keyboard=True,  # Allows the keyboard to resize dynamically
    input_field_placeholder="👇 Press the button",  # Placeholder text displayed in the input field
    selective=True,  # Ensures the keyboard is shown only to the specific users who triggered it
)

remove_keyboard = ReplyKeyboardRemove()
