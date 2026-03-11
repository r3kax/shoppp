from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def shop_kb(products):

    kb = InlineKeyboardMarkup()

    for p in products:

        kb.add(
        InlineKeyboardButton(
        text=f"{p[1]} | {p[2]}$",
        callback_data=f"buy_{p[0]}"
        ))

    return kb


def admin_kb():

    kb = InlineKeyboardMarkup()

    kb.add(
    InlineKeyboardButton("➕ Добавить товар",callback_data="admin_add_product")
    )

    kb.add(
    InlineKeyboardButton("📦 Добавить ключи",callback_data="admin_add_keys")
    )

    kb.add(
    InlineKeyboardButton("📊 Статистика",callback_data="admin_stats")
    )

    return kb