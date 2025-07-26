from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import currency_menu, to_currency_menu, language_menu
from utils import get_exchange_rate
from users import set_user_language, get_user_language
from messages import messages

class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()

async def start_handler(message: types.Message, state: FSMContext):
    set_user_language(message.from_user.id, "en")
    await state.finish()
    await message.answer("Choose your language:", reply_markup=language_menu())

async def language_handler(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    set_user_language(call.from_user.id, lang)
    await call.message.edit_text(messages["language_selected"][lang])
    await call.message.answer(messages["choose_currency"][lang], reply_markup=currency_menu())
    await CurrencyState.from_currency.set()

async def from_currency_handler(call: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(call.from_user.id)
    from_cur = call.data.split("_")[1]
    await state.update_data(from_currency=from_cur)
    await CurrencyState.to_currency.set()
    await call.message.edit_text(messages["choose_target_currency"][lang], reply_markup=to_currency_menu(from_cur))

async def to_currency_handler(call: types.CallbackQuery, state: FSMContext):
    lang = get_user_language(call.from_user.id)
    to_cur = call.data.split("_")[1]
    await state.update_data(to_currency=to_cur)
    await CurrencyState.amount.set()
    await call.message.edit_text(messages["enter_amount"][lang])

async def amount_handler(message: types.Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    data = await state.get_data()
    user_input = message.text.replace(",", ".").replace(" ", "")

    try:
        amount = float(user_input)
    except ValueError:
        await message.answer(messages["invalid_amount"][lang])
        return

    rate = await get_exchange_rate(data['from_currency'], data['to_currency'], amount)

    if rate == "connection_error":
        await message.answer(messages["connection_error"][lang])
        return
    if rate is None:
        await message.answer(messages["rate_not_found"][lang])
        return

    result = rate
    await message.answer(messages["result"][lang].format(
        amount=amount,
        from_cur=data['from_currency'],
        result=result,
        to_cur=data['to_currency']
    ))
    await message.answer(messages["choose_currency"][lang], reply_markup=currency_menu())
    await CurrencyState.from_currency.set()
