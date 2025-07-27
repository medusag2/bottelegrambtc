from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import currency_menu, to_currency_menu
from utils import get_exchange_rate

class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

def register_handlers(dp):
    dp.register_message_handler(start_handler, commands="start", state="*")
    dp.register_callback_query_handler(from_currency_handler, lambda c: c.data.startswith("from_"), state="*")
    dp.register_callback_query_handler(to_currency_handler, lambda c: c.data.startswith("to_"), state=CurrencyState.to_currency)
    dp.register_message_handler(amount_handler, state=CurrencyState.amount)

async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Valyutani tanlang:", reply_markup=currency_menu())

async def from_currency_handler(call: types.CallbackQuery, state: FSMContext):
    from_cur = call.data.split("_")[1]
    await state.update_data(from_currency=from_cur)
    await CurrencyState.to_currency.set()
    await call.message.edit_text("Qaysi valyutaga aylantiramiz?", reply_markup=to_currency_menu(from_cur))

async def to_currency_handler(call: types.CallbackQuery, state: FSMContext):
    to_cur = call.data.split("_")[1]
    await state.update_data(to_currency=to_cur)
    await CurrencyState.amount.set()
    await call.message.edit_text("Miqdorni kiriting:")

async def amount_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_input = message.text.replace(",", ".").replace(" ", "")

    try:
        amount = float(user_input)
    except ValueError:
        await message.answer("⛔ Faqat son kiriting. Masalan: 12500 yoki 12.5")
        return

    rate = await get_exchange_rate(data['from_currency'], data['to_currency'], amount)

    if rate == "connection_error":
        await message.answer("🌐 Valyuta xizmatiga ulanib bo‘lmadi.")
        return
    if rate is None:
        await message.answer("📉 Kurs topilmadi.")
        return

    result = rate
    await message.answer(f"✅ {amount} {data['from_currency']} = {result:.4f} {data['to_currency']}")
    await message.answer("Yana valyuta tanlang:", reply_markup=currency_menu())
    await CurrencyState.from_currency.set()
