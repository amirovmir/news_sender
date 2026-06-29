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


async def _fetch_feed(
    session: aiohttp.ClientSession, name: str, url: str
) -> list[tuple[str, str, str]]:
    """Returns list of (title, link, source_name)."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            content = await resp.text()
        feed = feedparser.parse(content)
        items = []
        for e in feed.entries[:5]:
            title = e.get("title", "")
            link = e.get("link", "")
            if title:
                items.append((title, link, name))
        return items
    except Exception as e:
        logger.warning(f"RSS {name} unavailable: {e}")
        return []


async def fetch_raw_headlines() -> list[tuple[str, str, str]]:
    """Returns list of (title, link, source_name), deduplicated by title."""
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_feed(session, name, url) for name, url in RSS_FEEDS.items()]
        results = await asyncio.gather(*tasks)

    seen: set[str] = set()
    unique: list[tuple[str, str, str]] = []
    for items in results:
        for title, link, source in items:
            if title not in seen:
                seen.add(title)
                unique.append((title, link, source))
    return unique[:20]


def _format_news_with_sources(items: list[tuple[str, str, str]], limit: int = 7) -> str:
    lines = []
    for i, (title, link, source) in enumerate(items[:limit], 1):
        if link:
            lines.append(f"{i}. {title}\n   <a href=\"{link}\">{source}</a>")
        else:
            lines.append(f"{i}. {title}\n   {source}")
    return "\n\n".join(lines)


async def get_news_summary(summarize_fn: Callable[[list[str]], Awaitable[str]]) -> str:
    items = await fetch_raw_headlines()
    if not items:
        return "📰 <b>Новости</b>\n⚠️ Новости временно недоступны"
    try:
        headlines_only = [title for title, _, _ in items]
        summary_text = await summarize_fn(headlines_only)
        # Append original headlines with source links below the summary
        sources_block = _format_news_with_sources(items)
        return f"📰 <b>Главные новости</b>\n\n{summary_text}\n\n<b>Источники:</b>\n\n{sources_block}"
    except Exception as e:
        logger.error(f"News summary error: {e}")
        return f"📰 <b>Главные новости</b>\n\n{_format_news_with_sources(items)}"
