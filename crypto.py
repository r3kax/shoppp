import aiohttp
from config import CRYPTO_TOKEN

async def create_invoice(amount):

    url = "https://pay.crypt.bot/api/createInvoice"

    headers = {
        "Crypto-Pay-API-Token":CRYPTO_TOKEN
    }

    data = {
        "asset":"USDT",
        "amount":amount
    }

    async with aiohttp.ClientSession() as session:

        async with session.post(url,json=data,headers=headers) as resp:

            r = await resp.json()

            return r["result"]