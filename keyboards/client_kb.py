from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton("/Working_hours")
button2 = KeyboardButton("/Address")
button3 = KeyboardButton("/Menu")
button4 = KeyboardButton("Send number", request_contact=True)
button5 = KeyboardButton("Send location", request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(button1, button2, button3).row(button4, button5)
