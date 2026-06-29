from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.database import get_user, update_user_city, update_user_time, toggle_user_active
from bot.keyboards.inline import main_menu, settings_menu
from bot.services.weather import geocode_city, get_weather_text
from bot.services.news import get_news_text

router = Router()


class SettingsState(StatesGroup):
    waiting_city = State()
    waiting_time = State()


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("Главное меню:", reply_markup=main_menu())


@router.callback_query(F.data == "weather")
async def cb_weather(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        await call.message.answer("Сначала напиши /start")
        return
    text = await get_weather_text(user.city_lat, user.city_lon, user.city_name)
    await call.message.answer(f"🌍 <b>Погода в {user.city_name}</b>\n{text}")


@router.callback_query(F.data == "news")
async def cb_news(call: CallbackQuery):
    await call.answer()
    await call.message.answer("⏳ Собираю новости...")
    text = await get_news_text()
    await call.message.answer(f"📰 <b>Главные новости</b>\n\n{text}")


@router.callback_query(F.data == "settings")
async def cb_settings(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        await call.message.answer("Сначала напиши /start")
        return
    status = "✅ включены" if user.is_active else "❌ выключены"
    text = (
        f"⚙️ <b>Настройки</b>\n\n"
        f"🏙 Город: <b>{user.city_name}</b>\n"
        f"⏰ Время: <b>{user.notification_time} (МСК)</b>\n"
        f"🔔 Уведомления: <b>{status}</b>"
    )
    await call.message.edit_text(text, reply_markup=settings_menu())


@router.callback_query(F.data == "set_city")
async def cb_set_city(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("🏙 Напиши название города (например: Москва, Казань, Новосибирск):")
    await state.set_state(SettingsState.waiting_city)


@router.message(SettingsState.waiting_city)
async def process_city(message: Message, state: FSMContext, scheduler: AsyncIOScheduler):
    await state.clear()
    result = await geocode_city(message.text.strip())
    if result is None:
        await message.answer("❌ Город не найден. Попробуй ещё раз: /settings")
        return
    lat, lon, display_name = result
    await update_user_city(message.from_user.id, display_name, lat, lon)
    from bot.services.scheduler import reschedule_user
    user = await get_user(message.from_user.id)
    reschedule_user(scheduler, message.bot, user.telegram_id, user.notification_time, lat, lon, display_name, user.is_active)
    weather = await get_weather_text(lat, lon, display_name)
    await message.answer(
        f"✅ Город изменён на <b>{display_name}</b>\n\n🌍 <b>Погода в {display_name}</b>\n{weather}",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "set_time")
async def cb_set_time(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        "⏰ Введи время уведомлений в формате <b>ЧЧ:ММ</b> по московскому времени (МСК).\n"
        "Например: <code>07:00</code>, <code>08:30</code>"
    )
    await state.set_state(SettingsState.waiting_time)


@router.message(SettingsState.waiting_time)
async def process_time(message: Message, state: FSMContext, scheduler: AsyncIOScheduler):
    time_str = message.text.strip()
    try:
        parts = time_str.split(":")
        assert len(parts) == 2
        h, m = int(parts[0]), int(parts[1])
        assert 0 <= h <= 23 and 0 <= m <= 59
        formatted = f"{h:02d}:{m:02d}"
    except Exception:
        await message.answer("❌ Неверный формат. Введи время в формате ЧЧ:ММ, например: <code>07:00</code>")
        return
    await state.clear()
    await update_user_time(message.from_user.id, formatted)
    from bot.services.scheduler import reschedule_user
    user = await get_user(message.from_user.id)
    reschedule_user(scheduler, message.bot, user.telegram_id, formatted, user.city_lat, user.city_lon, user.city_name, user.is_active)
    await message.answer(
        f"✅ Время уведомлений изменено на <b>{formatted} МСК</b>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "toggle_notifications")
async def cb_toggle(call: CallbackQuery, scheduler: AsyncIOScheduler):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        return
    new_state = not user.is_active
    await toggle_user_active(call.from_user.id, new_state)
    from bot.services.scheduler import reschedule_user
    user_after = await get_user(call.from_user.id)
    reschedule_user(scheduler, call.bot, user_after.telegram_id, user_after.notification_time, user_after.city_lat, user_after.city_lon, user_after.city_name, new_state)
    status = "✅ включены" if new_state else "❌ выключены"
    await call.message.answer(f"🔔 Уведомления теперь <b>{status}</b>")
