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


def _make_mock_session(rss_content: str):
    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=rss_content)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)
    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    return mock_session


@pytest.mark.asyncio
async def test_fetch_raw_headlines_returns_list():
    with patch("aiohttp.ClientSession", return_value=_make_mock_session(FAKE_RSS)):
        from bot.services.news import fetch_raw_headlines
        result = await fetch_raw_headlines()

    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, tuple) and len(item) == 3 for item in result)


@pytest.mark.asyncio
async def test_fetch_raw_headlines_deduplicates():
    with patch("aiohttp.ClientSession", return_value=_make_mock_session(FAKE_RSS)):
        from bot.services.news import fetch_raw_headlines
        result = await fetch_raw_headlines()

    titles = [title for title, _, _ in result]
    assert len(titles) == len(set(titles)), "Headlines should be deduplicated"


@pytest.mark.asyncio
async def test_get_news_text_contains_headlines_and_links():
    with patch("aiohttp.ClientSession", return_value=_make_mock_session(FAKE_RSS)):
        from bot.services.news import get_news_text
        result = await get_news_text()

    assert "Новость" in result
    assert "https://example.com" in result


@pytest.mark.asyncio
async def test_get_news_text_unavailable():
    empty_rss = """<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>"""
    with patch("aiohttp.ClientSession", return_value=_make_mock_session(empty_rss)):
        from bot.services.news import get_news_text
        result = await get_news_text()

    assert "недоступны" in result
