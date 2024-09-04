from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


# Creating an instance of Router specifically for handling admin-related messages
router = Router()

# Applying the AdminFilter to the message handler of the admin_router
# This ensures that only messages from admin users will be processed by this router


# Defining an asynchronous handler function for the /start command for admin users
# This function will be called when an admin user sends the /start command
@router.message(CommandStart())
async def admin_start(message: Message):
    # Replying to the admin user with a congratulatory message
    await message.reply("Congratulations, admin!")
