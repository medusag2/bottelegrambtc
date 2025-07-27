from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def currency_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton("USD", callback_data="from_USD"),
        InlineKeyboardButton("EUR", callback_data="from_EUR"),
        InlineKeyboardButton("RUB", callback_data="from_RUB"),
        InlineKeyboardButton("UZS", callback_data="from_UZS"),
    ]
    kb.add(*buttons)
    return kb

def to_currency_menu(from_currency):
    kb = InlineKeyboardMarkup(row_width=3)
    currencies = ["USD", "EUR", "RUB", "UZS"]
    buttons = [
        InlineKeyboardButton(cur, callback_data=f"to_{cur}")
        for cur in currencies if cur != from_currency
    ]
    kb.add(*buttons)
    return kb
