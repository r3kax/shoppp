from aiogram import Bot,Dispatcher,types
from aiogram.utils import executor
import database
import crypto
from config import *
from keyboards import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg:types.Message):

    await msg.answer("🛍 Магазин")


@dp.message_handler(commands=["shop"])
async def shop(msg:types.Message):

    products = database.get_products()

    kb = shop_kb(products)

    await msg.answer(
    "Выберите товар",
    reply_markup=kb
    )


@dp.callback_query_handler(lambda c:c.data.startswith("buy"))
async def buy(call:types.CallbackQuery):

    product_id = int(call.data.split("_")[1])

    products = database.get_products()

    product = [p for p in products if p[0]==product_id][0]

    invoice = await crypto.create_invoice(
    product[2],
    f"{call.from_user.id}:{product_id}"
    )

    kb = types.InlineKeyboardMarkup()

    kb.add(
    types.InlineKeyboardButton(
    text="💳 Оплатить",
    url=invoice["pay_url"]
    ))

    await call.message.answer(
    f"""
Товар: {product[1]}
Цена: {product[2]}$

После оплаты вы получите товар автоматически
""",
    reply_markup=kb
    )


executor.start_polling(dp)