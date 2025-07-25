from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def currency_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    currencies = ["USD", "EUR", "UZS", "BTC", "ETH", "USDT"]
    for c in currencies:
        markup.insert(InlineKeyboardButton(text=c, callback_data=f"from_{c}"))
    return markup

def to_currency_menu(selected_from):
    markup = InlineKeyboardMarkup(row_width=2)
    currencies = ["USD", "EUR", "UZS", "BTC", "ETH", "USDT"]
    for c in currencies:
        if c != selected_from:
            markup.insert(InlineKeyboardButton(text=c, callback_data=f"to_{c}"))
    markup.add(InlineKeyboardButton(text="🔙 Back", callback_data="back"))
    return markup
