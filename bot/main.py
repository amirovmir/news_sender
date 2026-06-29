import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from bot.config import settings
from bot.handlers import commands, callbacks, messages
from bot.services.scheduler import setup_scheduler


async def main():
    logger.info("Starting bot...")

    storage = RedisStorage.from_url(settings.redis_url)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(messages.router)  # catch-all последний

    scheduler = AsyncIOScheduler()
    scheduler.start()
    await setup_scheduler(scheduler, bot)

    logger.info("Bot is running!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown()
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
