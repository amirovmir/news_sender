import asyncio
from typing import Callable, Awaitable
import aiohttp
import feedparser
from loguru import logger

RSS_FEEDS = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
    "Мировые новости": "https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru",
}


async def _fetch_feed(session: aiohttp.ClientSession, name: str, url: str) -> list[str]:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            content = await resp.text()
        feed = feedparser.parse(content)
        return [e.get("title", "") for e in feed.entries[:5] if e.get("title")]
    except Exception as e:
        logger.warning(f"RSS {name} unavailable: {e}")
        return []


async def fetch_raw_headlines() -> list[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_feed(session, name, url) for name, url in RSS_FEEDS.items()]
        results = await asyncio.gather(*tasks)

    seen = set()
    unique = []
    for headlines in results:
        for h in headlines:
            if h not in seen:
                seen.add(h)
                unique.append(h)
    return unique[:20]


async def get_news_summary(summarize_fn: Callable[[list[str]], Awaitable[str]]) -> str:
    headlines = await fetch_raw_headlines()
    if not headlines:
        return "📰 <b>Новости</b>\n⚠️ Новости временно недоступны"
    try:
        summary = await summarize_fn(headlines)
        return f"📰 <b>Главные новости</b>\n\n{summary}"
    except Exception as e:
        logger.error(f"News summary error: {e}")
        numbered = "\n".join(f"{i}. {h}" for i, h in enumerate(headlines[:7], 1))
        return f"📰 <b>Главные новости</b>\n\n{numbered}"
