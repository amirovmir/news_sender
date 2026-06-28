import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_get_weather_text_returns_html():
    mock_response = {
        "current": {
            "temperature_2m": 20.5,
            "apparent_temperature": 19.0,
            "relative_humidity_2m": 65,
            "weather_code": 1,
            "wind_speed_10m": 3.2,
        },
        "daily": {
            "temperature_2m_max": [23.0],
            "temperature_2m_min": [15.0],
            "precipitation_sum": [0.0],
        },
    }

    mock_resp = AsyncMock()
    mock_resp.json = AsyncMock(return_value=mock_response)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.weather import get_weather_text
        result = await get_weather_text(55.7558, 37.6173, "Москва")

    assert "<b>" in result
    assert "Москва" in result
    assert "20.5" in result


@pytest.mark.asyncio
async def test_get_weather_text_fallback_on_error():
    with patch("aiohttp.ClientSession") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(side_effect=Exception("Network error"))
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        from bot.services.weather import get_weather_text
        result = await get_weather_text(55.7558, 37.6173, "Москва")

    assert "Москва" in result
    assert "недоступна" in result


@pytest.mark.asyncio
async def test_geocode_city_returns_none_on_empty():
    mock_response = {"results": []}

    mock_resp = AsyncMock()
    mock_resp.json = AsyncMock(return_value=mock_response)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.weather import geocode_city
        result = await geocode_city("НесуществующийГород12345")

    assert result is None


@pytest.mark.asyncio
async def test_geocode_city_returns_coords():
    mock_response = {
        "results": [{"latitude": 55.7558, "longitude": 37.6173, "name": "Москва", "country": "Россия"}]
    }

    mock_resp = AsyncMock()
    mock_resp.json = AsyncMock(return_value=mock_response)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        from bot.services.weather import geocode_city
        result = await geocode_city("Москва")

    assert result is not None
    lat, lon, name = result
    assert lat == 55.7558
    assert lon == 37.6173
    assert "Москва" in name
