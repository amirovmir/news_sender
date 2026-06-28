import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from loguru import logger

from bot.database import get_all_active_users
from bot.services.weather import get_weather_text
from bot.services.news import get_news_summary
from bot.services.ai_service import generate_motivation, summarize_headlines


async def send_morning_digest(bot: Bot, telegram_id: int, city_lat: float,
                               city_lon: float, city_name: str):
    try:
        motivation = await generate_motivation()
        weather = await get_weather_text(city_lat, city_lon, city_name)
        news = await get_news_summary(summarize_headlines)

        sep = "━" * 28
        text = (
            f"🌅 <b>Доброе утро!</b>\n\n"
            f"💪 {motivation}\n\n"
            f"{sep}\n\n"
            f"{weather}\n\n"
            f"{sep}\n\n"
            f"{news}\n\n"
            f"{sep}\n"
            f"💬 Напиши мне что-нибудь — я отвечу!"
        )
        await bot.send_message(telegram_id, text)
        logger.info(f"Morning digest sent to {telegram_id}")
    except Exception as e:
        logger.error(f"Failed to send digest to {telegram_id}: {e}")


def _parse_time(notification_time: str) -> tuple[int, int]:
    parts = notification_time.split(":")
    return int(parts[0]), int(parts[1])


def reschedule_user(scheduler: AsyncIOScheduler, bot: Bot, telegram_id: int,
                    notification_time: str, city_lat: float, city_lon: float,
                    city_name: str, is_active: bool):
    job_id = f"morning_{telegram_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    if not is_active:
        return
    hour, minute = _parse_time(notification_time)
    scheduler.add_job(
        send_morning_digest,
        trigger=CronTrigger(hour=hour, minute=minute, timezone="Europe/Moscow"),
        args=[bot, telegram_id, city_lat, city_lon, city_name],
        id=job_id,
        replace_existing=True,
    )


async def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot):
    users = await get_all_active_users()
    for user in users:
        reschedule_user(
            scheduler, bot,
            user.telegram_id, user.notification_time,
            user.city_lat, user.city_lon, user.city_name,
            user.is_active,
        )
    logger.info(f"Scheduler set up for {len(users)} active users")
