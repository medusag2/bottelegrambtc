import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import *
from aiogram.utils import executor  # Bu qismni tekshirib ko'ring


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.register_message_handler(start_handler, commands="start", state="*")
dp.register_callback_query_handler(from_currency_handler, lambda c: c.data.startswith("from_"), state="*")
dp.register_callback_query_handler(to_currency_handler, lambda c: c.data.startswith("to_"), state=CurrencyState.to_currency)
dp.register_callback_query_handler(back_handler, lambda c: c.data == "back", state="*")
dp.register_message_handler(amount_handler, state=CurrencyState.amount)

if name == '__main__':
    executor.start_polling(dp, skip_updates=True)
