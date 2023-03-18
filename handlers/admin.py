from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot
from data_base import sqlite_db


ID = None


# For creation of a menu item
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Get ID of current telegram group admin.
async def admin_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Ready for admin commands.")
    await message.delete()


# Start of new menu item creation
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Upload photo")


# Command for exiting from menu item creation process
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


# Acceptance of first stem of item creation (photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Now enter a name of the menu item")


# Accept second step (name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.reply("Now enter description")


# Accept third step (description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.reply("Now enter price")


# Accept the last step (price), and upload new menu item data to database
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = float(message.text)
    await sqlite_db.sql_add_command(state)
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=["Upload"], state=None)
    dp.register_message_handler(cancel_handler, commands="cancel", state="*")
    dp.register_message_handler(cancel_handler, (Text(equals="cancel", ignore_case=True)), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(admin_command, commands=["admin"], is_chat_admin=True)
