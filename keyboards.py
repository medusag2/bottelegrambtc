from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def currency_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    currencies = ["USD", "EUR", "RUB", "UZS", "BTC", "ETH"]
    buttons = [InlineKeyboardButton(cur, callback_data=f"from_{cur}") for cur in currencies]
    kb.add(*buttons)
    return kb

def to_currency_menu(from_currency):
    kb = InlineKeyboardMarkup(row_width=3)
    currencies = ["USD", "EUR", "RUB", "UZS", "BTC", "ETH"]
    buttons = [
        InlineKeyboardButton(cur, callback_data=f"to_{cur}")
        for cur in currencies if cur != from_currency
    ]
    buttons.append(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    kb.add(*buttons)
    return kb
