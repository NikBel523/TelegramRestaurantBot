import json
import string

from aiogram import types, Dispatcher


# filthy language filter
async def echo_send(message: types.Message):
    if {word.lower().translate(str.maketrans("", "", string.punctuation)) for word in message.text.split(" ")}\
            .intersection(set(json.load(open("censorship.json")))) != set():
        await message.reply("Please, be polite. Don't use this type of language in our group.")
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
