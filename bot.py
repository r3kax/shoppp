import asyncio
from aiogram import Bot,Dispatcher,types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from config import *
import database
import crypto

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

menu = types.ReplyKeyboardMarkup(
keyboard=[
["👤 Профиль"],
["🛒 Купить"],
["📦 Наличие"]
],
resize_keyboard=True
)

@dp.message(commands=["start"])
async def start(msg:types.Message):

    database.add_user(msg.from_user.id)

    await msg.answer(
"🛍 Добро пожаловать в магазин",
reply_markup=menu
)

@dp.message(lambda m:m.text=="📦 Наличие")
async def stock(msg:types.Message):

    products = database.get_products()

    text = "📦 Товары\n\n"

    for p in products:

        text+=f"{p[0]}. {p[1]} — {p[2]}$\n"

    await msg.answer(text)

@dp.message(lambda m:m.text=="🛒 Купить")
async def buy(msg:types.Message):

    products = database.get_products()

    kb = InlineKeyboardMarkup()

    for p in products:

        kb.add(
        InlineKeyboardButton(
        text=f"{p[1]} {p[2]}$",
        callback_data=f"buy_{p[0]}"
        ))

    await msg.answer(
"Выберите товар",
reply_markup=kb
)

@dp.callback_query(lambda c:c.data.startswith("buy"))
async def buy_item(call:types.CallbackQuery):

    product_id = int(call.data.split("_")[1])

    products = database.get_products()

    product = [p for p in products if p[0]==product_id][0]

    invoice = await crypto.create_invoice(product[2])

    pay_url = invoice["pay_url"]

    kb = InlineKeyboardMarkup()

    kb.add(
    InlineKeyboardButton(
    text="💳 Оплатить",
    url=pay_url
    ))

    await call.message.answer(
f"""
Товар: {product[1]}

Цена: {product[2]}$

После оплаты товар будет выдан автоматически
""",
reply_markup=kb
)

async def main():

    await dp.start_polling(bot)

asyncio.run(main())