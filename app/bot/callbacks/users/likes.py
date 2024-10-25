from aiogram import (
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from punq import Container

from app.bot.handlers.users.profile import profile
from app.bot.keyboards.inline import like_dislike_keyboard
from app.bot.utils.constants import (
    match_text_message,
    profile_text_message,
)
from app.domain.entities.users import UserEntity
from app.logic.init import init_container
from app.logic.services.base import (
    BaseLikesService,
    BaseUsersService,
)


callback_like_router = Router()


class UserSession:
    def __init__(self, users):
        self.users = users
        self.current_index = 0

    def has_more_users(self):
        return self.current_index < len(self.users)

    def get_next_user(self):
        if self.has_more_users():
            user = self.users[self.current_index]
            self.current_index += 1
            return user
        return None


async def send_user_profile(callback: CallbackQuery, user: UserEntity):
    await callback.message.answer_photo(
        photo=user.photo,
        caption=profile_text_message(user),
        reply_markup=like_dislike_keyboard(user_id=user.telegram_id),
    )


async def process_next_user(callback: CallbackQuery, session: UserSession):
    next_user = session.get_next_user()
    if next_user:
        await send_user_profile(callback, next_user)
    else:
        await callback.message.answer("That's all.")
        await profile(callback)


@callback_like_router.callback_query(
    lambda callback_query: callback_query.data.startswith("like_"),
)
async def handle_like_user(
    callback: CallbackQuery,
    state: FSMContext,
    container: Container = init_container(),
):
    likes_service: BaseLikesService = container.resolve(BaseLikesService)
    users_service: BaseUsersService = container.resolve(BaseUsersService)

    liked_user_id = int(callback.data.split("_")[1])
    user_liked = await users_service.get_user(liked_user_id)
    user_who_liked = await users_service.get_user(callback.from_user.id)

    await likes_service.create_like(
        from_user_id=user_who_liked.telegram_id,
        to_user_id=user_liked.telegram_id,
    )

    await callback.message.answer_photo(
        photo=user_liked.photo,
        caption=match_text_message(user_liked),
    )
    await likes_service.delete_like(
        from_user_id=user_who_liked.telegram_id,
        to_user_id=user_liked.telegram_id,
    )
    await likes_service.delete_like(
        from_user_id=user_liked.telegram_id,
        to_user_id=user_who_liked.telegram_id,
    )

    # Завантажуємо поточну сесію зі стану
    data = await state.get_data()
    session = data.get("session")

    # If the session exists, we continue to display the next user
    if session:
        await process_next_user(callback, session)


@callback_like_router.callback_query(
    lambda callback_query: callback_query.data.startswith("dislike_"),
)
async def handle_dislike_user(
    callback: CallbackQuery,
    state: FSMContext,
    container: Container = init_container(),
):
    likes_service: BaseLikesService = container.resolve(BaseLikesService)

    disliked_user_id = int(callback.data.split("_")[1])
    await likes_service.delete_like(
        from_user_id=disliked_user_id,
        to_user_id=callback.from_user.id,
    )

    # We load the current session from the state
    data = await state.get_data()
    session = data.get("session")

    # We continue processing with the current session
    if session:
        await process_next_user(callback, session)


@callback_like_router.callback_query(F.data == "see_who_liked")
async def handle_see_who_liked(
    callback: CallbackQuery,
    state: FSMContext,
    container: Container = init_container(),
):
    likes_service: BaseLikesService = container.resolve(BaseLikesService)
    users_service: BaseUsersService = container.resolve(BaseUsersService)

    likes = await likes_service.get_users_ids_liked_by(callback.from_user.id)

    if likes:
        liked_users = [await users_service.get_user(user_id) for user_id in likes]

        session = UserSession(liked_users)

        # We save the session in the user state
        await state.update_data(session=session)

        await process_next_user(callback, session)
    else:
        await callback.message.answer("No likes found.")
