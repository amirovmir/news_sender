import asyncio
import html
from groq import Groq
import google.generativeai as genai
from loguru import logger
from bot.config import settings

_groq = Groq(api_key=settings.groq_api_key)
genai.configure(api_key=settings.gemini_api_key)
_gemini = genai.GenerativeModel(settings.gemini_model)

SYSTEM_PROMPT = (
    "Ты дружелюбный и умный ассистент в Telegram-боте. "
    "Отвечай на русском языке. Будь кратким и информативным. "
    "Не используй никакого форматирования: никаких звёздочек, подчёркиваний, жирного или курсивного текста. "
    "Для блоков кода используй только <code>...</code>."
)


def _groq_messages(question: str, history: list[dict]) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})
    return messages


async def _ask_groq(question: str, history: list[dict]) -> str:
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: _groq.chat.completions.create(
            model=settings.groq_model,
            messages=_groq_messages(question, history),
            temperature=0.7,
            max_tokens=1500,
        ),
    )
    return response.choices[0].message.content


async def _ask_gemini(question: str, history: list[dict]) -> str:
    context = "\n".join(
        f"{'Пользователь' if m['role'] == 'user' else 'Ассистент'}: {m['content']}"
        for m in history[-6:]
    )
    prompt = f"{SYSTEM_PROMPT}\n\n{context}\nПользователь: {question}" if context else f"{SYSTEM_PROMPT}\n\nПользователь: {question}"
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: _gemini.generate_content(prompt),
    )
    return response.text


async def ask(question: str, history: list[dict] | None = None) -> str:
    history = history or []
    try:
        return await _ask_groq(question, history)
    except Exception as e:
        logger.warning(f"Groq failed, falling back to Gemini: {e}")
        try:
            return await _ask_gemini(question, history)
        except Exception as e2:
            logger.error(f"Gemini also failed: {e2}")
            return "⚠️ Сервис временно недоступен. Попробуйте позже."


async def generate_motivation() -> str:
    prompt = (
        "Назови одну реальную вдохновляющую цитату известного человека на русском языке. "
        "Ответь строго в формате двух строк:\n"
        "Строка 1: сам текст цитаты, без кавычек\n"
        "Строка 2: имя автора, без тире и дополнительных слов\n"
        "Больше ничего не добавляй."
    )
    try:
        raw = await _ask_groq(prompt, [])
        lines = [line.strip().strip('"«»') for line in raw.strip().splitlines() if line.strip()]
        if len(lines) >= 2:
            quote, author = html.escape(lines[0]), html.escape(lines[1])
        else:
            quote, author = html.escape(lines[0]), ""
        return f"<blockquote>{quote}</blockquote>— {author}" if author else f"<blockquote>{quote}</blockquote>"
    except Exception:
        return "<blockquote>Делай что должен, и будь что будет.</blockquote>— Марк Аврелий"


async def translate_headlines(headlines: list[str]) -> list[str]:
    """Translate headlines to Russian. Returns original list on failure."""
    if not headlines:
        return headlines
    numbered = "\n".join(f"{i}. {h}" for i, h in enumerate(headlines, 1))
    prompt = (
        f"Переведи следующие заголовки новостей на русский язык. "
        f"Верни ТОЛЬКО пронумерованный список в том же порядке, без пояснений:\n{numbered}"
    )
    try:
        raw = await _ask_groq(prompt, [])
        translated = []
        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip leading "1. ", "1) ", etc.
            if line[0].isdigit():
                line = line.split(".", 1)[-1].split(")", 1)[-1].strip()
            translated.append(line)
        if len(translated) == len(headlines):
            return translated
        logger.warning(f"Translation count mismatch: {len(headlines)} in, {len(translated)} out")
        return headlines
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return headlines
