from aiogram import (
    Bot,
    F,
    Router,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from punq import Container

from app.bot.handlers.users.profile import profile
from app.bot.keyboards.reply import remove_keyboard
from app.bot.utils.states import (
    UserAboutUpdate,
    UserPhotoUpdate,
)
from app.domain.exceptions.base import ApplicationException
from app.domain.values.users import AboutText
from app.infra.s3.base import BaseS3Storage
from app.logic.init import init_container
from app.logic.services.base import BaseUsersService


profile_edit_router = Router()


@profile_edit_router.message(UserAboutUpdate.about)
async def about_edit_state(
    message: Message,
    state: FSMContext,
    container: Container = init_container(),
):
    service: BaseUsersService = container.resolve(BaseUsersService)
    try:
        if message.text.lower() == "🪪 skip":
            about = AboutText(None)
        else:
            about = AboutText(message.text)
        await state.clear()
        await message.answer(
            "You have successfully updated your details.",
            reply_markup=remove_keyboard,
        )

        await service.update_user_about_info(
            telegram_id=message.from_user.id,
            about=about,
        )

        await profile(message)
    except ApplicationException as exception:
        await message.answer(text=exception.message + " Enter the text again.")


@profile_edit_router.message(UserPhotoUpdate.photo, F.photo)
async def photo_edit(
    message: Message,
    state: FSMContext,
    bot: Bot,
    container: Container = init_container(),
):
    uploader: BaseS3Storage = container.resolve(BaseS3Storage)
    service: BaseUsersService = container.resolve(BaseUsersService)
    await state.clear()

    photo_file_id = message.photo[-1].file_id
    file = await bot.get_file(photo_file_id)
    file_path = file.file_path
    photo_file_stream = await bot.download_file(file_path)
    photo_file_bytes = photo_file_stream.read()

    photo_url = await uploader.upload_file(
        file=photo_file_bytes,
        file_name=f"{message.from_user.id}.png",
    )

    await service.update_user_info_after_reg(
        telegram_id=message.from_user.id,
        data={"photo": photo_url},
    )

    await profile(message)


@profile_edit_router.message(UserPhotoUpdate.photo, ~F.photo)
async def user_photo_error(message: Message):
    await message.answer("Send a photo!")
