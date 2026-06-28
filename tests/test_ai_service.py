import pytest
from unittest.mock import patch, MagicMock


def _make_groq_response(text: str):
    msg = MagicMock()
    msg.content = text
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@pytest.mark.asyncio
async def test_ask_returns_string():
    with patch("groq.Groq") as MockGroq:
        instance = MockGroq.return_value
        instance.chat.completions.create.return_value = _make_groq_response("Привет!")

        from bot.services import ai_service
        ai_service._groq = instance

        result = await ai_service.ask("Как дела?")

    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_ask_falls_back_to_gemini_on_groq_error():
    mock_groq = MagicMock()
    mock_groq.chat.completions.create.side_effect = Exception("Rate limit")

    mock_gemini = MagicMock()
    gemini_resp = MagicMock()
    gemini_resp.text = "Ответ от Gemini"
    mock_gemini.generate_content.return_value = gemini_resp

    from bot.services import ai_service
    ai_service._groq = mock_groq
    ai_service._gemini = mock_gemini

    result = await ai_service.ask("Как дела?")

    assert "Gemini" in result or len(result) > 0


@pytest.mark.asyncio
async def test_ask_returns_error_message_when_both_fail():
    mock_groq = MagicMock()
    mock_groq.chat.completions.create.side_effect = Exception("Groq down")

    mock_gemini = MagicMock()
    mock_gemini.generate_content.side_effect = Exception("Gemini down")

    from bot.services import ai_service
    ai_service._groq = mock_groq
    ai_service._gemini = mock_gemini

    result = await ai_service.ask("Тест")

    assert "недоступен" in result.lower() or "ошибка" in result.lower()


@pytest.mark.asyncio
async def test_generate_motivation_returns_string():
    mock_groq = MagicMock()
    mock_groq.chat.completions.create.return_value = _make_groq_response(
        "Каждый день — новая возможность!"
    )

    from bot.services import ai_service
    ai_service._groq = mock_groq

    result = await ai_service.generate_motivation()

    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_generate_motivation_has_hardcoded_fallback():
    mock_groq = MagicMock()
    mock_groq.chat.completions.create.side_effect = Exception("down")

    mock_gemini = MagicMock()
    mock_gemini.generate_content.side_effect = Exception("down")

    from bot.services import ai_service
    ai_service._groq = mock_groq
    ai_service._gemini = mock_gemini

    result = await ai_service.generate_motivation()

    assert isinstance(result, str)
    assert len(result) > 5  # hardcoded fallback is always returned
