from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

TOKEN = os.environ.get("TELEGRAM_RESTAURANT_BOT")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=True)
