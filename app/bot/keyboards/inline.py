from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_inline_kb(user_id, liked_by):
    builder = InlineKeyboardBuilder()
    if liked_by:
        builder.row(
            InlineKeyboardButton(
                text="You were liked by 💌",
                callback_data="see_who_liked",
            ),
        )
    builder.row(
        InlineKeyboardButton(text="Edit your profile ⚙️", callback_data="profile_edit"),
    )
    builder.row(
        InlineKeyboardButton(text="💗 View surveys", callback_data="view"),
    )
    return builder.as_markup()


def profile_edit_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1",
                    callback_data="profile_page",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="2",
                    callback_data="form",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="3",
                    callback_data="photo_edit",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="4",
                    callback_data="about_edit",
                    one_time=True,
                ),
            ],
        ],
    )
    return keyboard


def re_registration_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes ✅",
                    callback_data="form_confirm",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="No ❎",
                    callback_data="profile_edit",
                    one_time=True,
                ),
            ],
        ],
    )
    return keyboard


def photo_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes ✅",
                    callback_data="photo_confirm",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="No ❎",
                    callback_data="profile_edit",
                    one_time=True,
                ),
            ],
        ],
    )
    return keyboard


def about_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes ✅",
                    callback_data="about_confirm",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="No ❎",
                    callback_data="profile_edit",
                    one_time=True,
                ),
            ],
        ],
    )
    return keyboard


def liked_by_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes ✅",
                    callback_data="see_who_liked",
                ),
                InlineKeyboardButton(
                    text="No ❎",
                    callback_data="profile_page",
                ),
            ],
        ],
    )
    return keyboard


def like_dislike_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👍",
                    callback_data=f"like_{user_id}",
                    one_time=True,
                ),
                InlineKeyboardButton(
                    text="👎",
                    callback_data=f"dislike_{user_id}",
                    one_time=True,
                ),
            ],
        ],
    )
    return keyboard
