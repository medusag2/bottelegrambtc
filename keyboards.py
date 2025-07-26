from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def currency_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    currencies = ["USD", "EUR", "UZS", "RUB"]  # RUB qo‘shildi
    for cur in currencies:
        markup.insert(InlineKeyboardButton(cur, callback_data=f"from_{cur}"))
    return markup

def to_currency_menu(from_currency):
    markup = InlineKeyboardMarkup(row_width=2)
    currencies = ["USD", "EUR", "UZS", "RUB"]
    for cur in currencies:
        if cur != from_currency:
            markup.insert(InlineKeyboardButton(cur, callback_data=f"to_{cur}"))
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back"))
    return markup
