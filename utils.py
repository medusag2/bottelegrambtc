import aiohttp
async def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            rate = data.get("result")
            if rate is None:
                raise ValueError("Exchange rate not found.")
            return rate
