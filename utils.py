from config import EXCHANGE_API_KEY
import aiohttp

async def get_exchange_rate(from_currency: str, to_currency: str, amount: float):
    url = f"https://api.exchangerate.host/convert?access_key={EXCHANGE_API_KEY}&from={from_currency}&to={to_currency}&amount={amount}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"❌ API ulanish muammosi: HTTP {resp.status}")
                    return "connection_error"

                data = await resp.json()
                converted_amount = data.get("result")  # ✅ Bu tayyor qiymat

                if converted_amount is None:
                    print("❌ Kurs topilmadi")
                    return None

                print(f"✅ API javobi: {converted_amount}")
                return converted_amount  # ✅ To‘g‘ridan-to‘g‘ri natija qaytaryapti

    except aiohttp.ClientError as e:
        print(f"❌ API client xatosi: {e}")
        return "connection_error"
    except Exception as e:
        print(f"❌ Noma'lum xato: {e}")
        return None
