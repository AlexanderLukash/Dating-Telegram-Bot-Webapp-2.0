from app.bot.keyboards.inline import liked_by_keyboard
from app.bot.main import bot


async def send_liked_message(
    to_user_id: int,
):
    await bot.send_message(
        to_user_id,
        text="<b>You were liked 💗</b>\nDo you want to see those who liked you?",
        reply_markup=liked_by_keyboard(),
    )
