from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import get_or_create_user, get_user
from bot.keyboards.inline import main_menu, settings_menu
from bot.services.weather import get_weather_text
from bot.services.news import get_news_text

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await get_or_create_user(message.from_user.id, message.from_user.username)
    text = (
        "👋 <b>Привет!</b>\n\n"
        "Я твой утренний помощник. Каждое утро в <b>7:00 по Москве</b> я пришлю:\n"
        "💪 Мотивацию на день\n"
        "🌤 Прогноз погоды\n"
        "📰 Краткую сводку главных новостей\n\n"
        "А ещё можешь просто написать мне — я отвечу с помощью AI!\n\n"
        "Настрой город и время в /settings"
    )
    await message.answer(text, reply_markup=main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📋 <b>Команды:</b>\n\n"
        "/start — приветствие и регистрация\n"
        "/weather — текущая погода\n"
        "/news — сводка новостей\n"
        "/settings — настройки (город, время, уведомления)\n"
        "/help — эта справка\n\n"
        "Или просто напиши что-нибудь — я отвечу!"
    )
    await message.answer(text)


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала напиши /start")
        return
    await message.answer("⏳ Запрашиваю погоду...")
    text = await get_weather_text(user.city_lat, user.city_lon, user.city_name)
    await message.answer(f"🌍 <b>Погода в {user.city_name}</b>\n{text}")


@router.message(Command("news"))
async def cmd_news(message: Message):
    await message.answer("⏳ Собираю новости...")
    text = await get_news_text()
    await message.answer(f"📰 <b>Главные новости</b>\n\n{text}")


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала напиши /start")
        return
    status = "✅ включены" if user.is_active else "❌ выключены"
    text = (
        f"⚙️ <b>Настройки</b>\n\n"
        f"🏙 Город: <b>{user.city_name}</b>\n"
        f"⏰ Время уведомлений: <b>{user.notification_time} (МСК)</b>\n"
        f"🔔 Уведомления: <b>{status}</b>"
    )
    await message.answer(text, reply_markup=settings_menu())
