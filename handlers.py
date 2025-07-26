from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import currency_menu, to_currency_menu
from utils import get_exchange_rate

from messages import messages

lang = user_lang or "uz"  # har bir foydalanuvchining tilini aniqlang

await message.answer(messages["start"][lang])

class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("💱 Valyutani tanlang:", reply_markup=currency_menu())

async def from_currency_handler(call: types.CallbackQuery, state: FSMContext):
    from_cur = call.data.split("_")[1]
    await state.update_data(from_currency=from_cur)
    await CurrencyState.to_currency.set()
    await call.message.edit_text("🔁 Qaysi valyutaga aylantiramiz?", reply_markup=to_currency_menu(from_cur))

async def to_currency_handler(call: types.CallbackQuery, state: FSMContext):
    to_cur = call.data.split("_")[1]
    await state.update_data(to_currency=to_cur)
    await CurrencyState.amount.set()
    await call.message.edit_text("✍️ Miqdorni kiriting (faqat son):")

async def amount_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_input = message.text.replace(",", ".").replace(" ", "")

    try:
        amount = float(user_input)
    except ValueError:
        await message.answer("⛔ Format noto'g'ri! Masalan: `12500` yoki `12.5`")
        return

    converted = await get_exchange_rate(
        data['from_currency'], data['to_currency'], amount
    )

    if converted == "connection_error":
        await message.answer("🌐 Valyuta xizmatiga ulanib bo'lmadi. Iltimos, keyinroq urinib ko‘ring.")
        return

    if converted is None:
        await message.answer("📉 Valyuta kursi topilmadi. Iltimos, boshqa valyutani tanlang.")
        return

    await message.answer(
        f"✅ {amount} {data['from_currency']} = {converted:.4f} {data['to_currency']}"
    )
    await message.answer("Yana valyuta tanlang:", reply_markup=currency_menu())
    await CurrencyState.from_currency.set()

async def back_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("🔙 Valyutani tanlang:", reply_markup=currency_menu())
