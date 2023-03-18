from aiogram.utils import executor
from create_bot import dp
from handlers import other


async def on_startup(_):
    print("Bot online")



other.register_handlers_other(dp=dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

