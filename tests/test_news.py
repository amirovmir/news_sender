import pytest
from unittest.mock import AsyncMock, patch, MagicMock


FAKE_RSS = """<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <item><title>Новость первая</title><link>https://example.com/1</link></item>
    <item><title>Новость вторая</title><link>https://example.com/2</link></item>
    <item><title>Новость третья</title><link>https://example.com/3</link></item>
  </channel>
</rss>"""


@pytest.mark.asyncio
async def test_fetch_raw_headlines_returns_list():
    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=FAKE_RSS)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.news import fetch_raw_headlines
        result = await fetch_raw_headlines()

    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, tuple) and len(item) == 3 for item in result)


@pytest.mark.asyncio
async def test_fetch_raw_headlines_deduplicates():
    duplicate_rss = FAKE_RSS  # same feed for all sources → same headlines

    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=duplicate_rss)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.news import fetch_raw_headlines
        result = await fetch_raw_headlines()

    titles = [title for title, _, _ in result]
    assert len(titles) == len(set(titles)), "Headlines should be deduplicated"


@pytest.mark.asyncio
async def test_get_news_summary_uses_summarize_fn():
    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=FAKE_RSS)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    async def fake_summarize(headlines):
        return "Краткая сводка: " + ", ".join(headlines[:2])

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.news import get_news_summary
        result = await get_news_summary(fake_summarize)

    assert "📰" in result
    assert "Краткая сводка" in result


@pytest.mark.asyncio
async def test_get_news_summary_fallback_on_summarize_error():
    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=FAKE_RSS)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    async def broken_summarize(headlines):
        raise RuntimeError("AI unavailable")

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.news import get_news_summary
        result = await get_news_summary(broken_summarize)

    assert "📰" in result
    assert "Новость" in result  # fallback numbered list
