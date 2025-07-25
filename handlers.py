from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import currency_menu, to_currency_menu
from utils import get_exchange_rate

class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

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
    try:
        # foydalanuvchi 1 000 yoki 1,000 deb yozsa ham float'ga aylansin
        cleaned_text = message.text.replace(",", ".").replace(" ", "")
        amount = float(cleaned_text)

        rate = await get_exchange_rate(data['from_currency'], data['to_currency'])

        if rate is None:
            raise ValueError("Exchange rate not found.")

        result = amount * rate
        await message.answer(f"{amount} {data['from_currency']} = {result:.4f} {data['to_currency']}")
        await message.answer("Yana valyuta tanlang:", reply_markup=currency_menu())
        await CurrencyState.from_currency.set()

    except Exception as e:
        print(f"❌ Xatolik: {e}")  # Railway log'da ko'rasiz
        await message.answer("Noto‘g‘ri qiymat! Iltimos, faqat raqam kiriting.")

async def back_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Valyutani tanlang:", reply_markup=currency_menu())
