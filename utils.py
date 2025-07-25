import aiohttp

async def get_exchange_rate(from_currency, to_currency):
    get_exchange_rate(from_currency, to_currency)
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&access_key={EXCHANGE_API_KEY}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"❌ API ulanish muammosi: HTTP {resp.status}")
                    return "connection_error"

                data = await resp.json()
                rate = data.get("result")

                if rate is None:
                    print("❌ Kurs topilmadi")
                    return None

                print(f"✅ API javobi: {rate}")
                return rate

    except aiohttp.ClientError as e:
        print(f"❌ API client xatosi: {e}")
        return "connection_error"
    except Exception as e:
        print(f"❌ Noma'lum xato: {e}")
        return None
