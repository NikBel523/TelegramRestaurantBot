from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb

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
    await bot.send_message(message.from_user.id, "Ready for admin commands.", reply_markup=admin_kb.button_case_admin)
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


# Delete chosen menu item
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} deleted.", show_alert=True)


# Show all menu items to admin with inline "Delete" buttons
@dp.message_handler(commands="Delete")
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.admin_menu_read()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nDescription: {ret[2]}\nPrice {ret[-1]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup()
                                   .add(InlineKeyboardButton(f"Delete {ret[1]}", callback_data=f"del {ret[1]}"))
                                   )


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=["Upload"], state=None)
    dp.register_message_handler(cancel_handler, commands="cancel", state="*")
    dp.register_message_handler(cancel_handler, (Text(equals="cancel", ignore_case=True)), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(admin_command, commands=["admin"], is_chat_admin=True)
