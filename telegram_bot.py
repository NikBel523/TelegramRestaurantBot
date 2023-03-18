from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db


async def on_startup(_):
    print("Bot online")
    sqlite_db.sql_start()


client.register_handlers_client(dp=dp)
admin.register_handlers_admin(dp=dp)
other.register_handlers_other(dp=dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
