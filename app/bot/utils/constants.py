from aiogram.types import User

from app.domain.entities.users import UserEntity


def first_welcome_message(user: User) -> str:
    message: str = f"""Welcome, <b>{user.first_name}</b> to our dating bot. 
To get started, fill out your profile using the command: <b>/form</b>"""
    return message


def second_welcome_message(user: User):
    message: str = f"""Welcome back <b>{user.first_name}</b> to our bot. 
It looks like your account is not active, so please fill it in using the command first: <b>/form</b>"""
    return message


def user_profile_text_message(user: UserEntity) -> str:
    profile_text = (
        f"<b>✨ Your survey:</b> \n\n"
        f"<b>👋 Name:</b> {user.name} | @{user.username}\n"
        f"<b>🎀 Age:</b> {user.age}\n"
        f"<b>🌆 City:</b> {user.city}\n"
        f"<b>👫 Gender:</b> {user.gender}\n"
    )

    if user.about:
        profile_text += f"<b>✍️ About you:</b> \n" f"<i>{user.about}</i>"

    return profile_text


def profile_text_message(user: UserEntity) -> str:
    profile_text = (
        f"\n<b>👋 Name:</b> {user.name}\n"
        f"<b>🎀 Age:</b> {user.age}\n"
        f"<b>🌆 City:</b> {user.city}\n"
        f"<b>👫 Gender:</b> {user.gender}\n"
    )

    if user.about:
        profile_text += f"<b>✍️ About user:</b> \n" f"<i>{user.about}</i>"

    return profile_text
