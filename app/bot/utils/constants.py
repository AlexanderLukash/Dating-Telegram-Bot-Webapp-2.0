from aiogram.types import User


def first_welcome_message(user: User) -> str:
    message: str = f"""Welcome, <b>{user.first_name}</b> to our dating bot. 
To get started, fill out your profile using the command: <b>/form</b>"""
    return message


def second_welcome_message(user: User):
    message: str = f"""Welcome back <b>{user.first_name}</b> to our bot. 
It looks like your account is not active, so please fill it in using the command first: <b>/form</b>"""
    return message
