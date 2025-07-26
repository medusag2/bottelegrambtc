from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def currency_menu():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🇺🇸 USD", callback_data="from_USD"),
        InlineKeyboardButton("🇪🇺 EUR", callback_data="from_EUR"),
        InlineKeyboardButton("🇷🇺 RUB", callback_data="from_RUB"),
        InlineKeyboardButton("🇬🇧 GBP", callback_data="from_GBP")
    )

def to_currency_menu(from_cur):
    return InlineKeyboardMarkup(row_width=2).add(
        *[
            InlineKeyboardButton(text, callback_data=f"to_{code}")
            for code, text in {
                "USD": "🇺🇸 USD",
                "EUR": "🇪🇺 EUR",
                "RUB": "🇷🇺 RUB",
                "GBP": "🇬🇧 GBP"
            }.items() if code != from_cur
        ]
    )

def language_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    )
