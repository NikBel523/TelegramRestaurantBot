from aiogram import types, Dispatcher

from create_bot import bot
from data_base import sqlite_db


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Greetings!")
        await message.delete()
    except:
        await message.reply("In order to use bot, please send it a message first: \nhttps://t.me/example_restaurant_bot")


async def working_hours_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Working hours: 12:00 - 24:00")


async def address_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Cool Street 69")


# Show all menu items to client
async def show_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(working_hours_command, commands=["Working_hours"])
    dp.register_message_handler(address_command, commands=["Address"])
    dp.register_message_handler(show_menu_command, commands=["Menu"])
