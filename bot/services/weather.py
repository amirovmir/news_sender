import aiohttp
from loguru import logger

WEATHER_CODES = {
    0: "☀️ Ясно", 1: "🌤 Преим. ясно", 2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно", 45: "🌫 Туман", 48: "🌫 Изморозь",
    51: "🌦 Лёгкая морось", 61: "🌧 Небольшой дождь", 71: "🌨 Небольшой снег",
    80: "⛈ Ливень", 95: "⚡ Гроза",
}


async def geocode_city(city: str) -> tuple[float, float, str] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "ru", "format": "json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
        results = data.get("results")
        if not results:
            return None
        r = results[0]
        name = r.get("name", city)
        country = r.get("country", "")
        display = f"{name}, {country}" if country else name
        return r["latitude"], r["longitude"], display
    except Exception as e:
        logger.error(f"Geocode error for '{city}': {e}")
        return None


async def get_weather_text(lat: float, lon: float, city_name: str) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "Europe/Moscow",
        "forecast_days": 1,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()

        cur = data["current"]
        daily = data["daily"]
        code = cur.get("weather_code", 0)
        condition = WEATHER_CODES.get(code, "🌡")

        return (
            f"{condition} <b>{cur['temperature_2m']}°C</b> "
            f"(ощущается {cur['apparent_temperature']}°C)\n"
            f"💧 Влажность: {cur['relative_humidity_2m']}%\n"
            f"💨 Ветер: {cur['wind_speed_10m']} м/с\n"
            f"📊 Сегодня: макс {daily['temperature_2m_max'][0]}°C / "
            f"мин {daily['temperature_2m_min'][0]}°C, "
            f"осадки {daily['precipitation_sum'][0]} мм"
        )
    except Exception as e:
        logger.error(f"Weather error: {e}")
        return "⚠️ Погода временно недоступна"
