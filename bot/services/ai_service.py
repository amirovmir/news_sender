import asyncio
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
    "Используй HTML-теги для форматирования: <b>жирный</b>, <i>курсив</i>, <code>код</code>."
)


def _groq_messages(question: str, history: list[dict]) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})
    return messages


async def _ask_groq(question: str, history: list[dict]) -> str:
    loop = asyncio.get_event_loop()
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
    loop = asyncio.get_event_loop()
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
        "Напиши одну короткую мотивационную фразу на русском языке для утреннего сообщения. "
        "Позитивная, жизнеутверждающая, 1-2 предложения. Без кавычек."
    )
    try:
        return await _ask_groq(prompt, [])
    except Exception:
        return "Каждый новый день — это новая возможность стать лучше!"


async def summarize_headlines(headlines: list[str]) -> str:
    joined = "\n".join(f"- {h}" for h in headlines)
    prompt = (
        f"Вот заголовки новостей за последние сутки:\n{joined}\n\n"
        "Выдели 5 главных тем (не просто перечисли заголовки, а кратко опиши суть каждой темы). "
        "Формат: нумерованный список, 1-2 предложения на каждую тему. HTML не нужен, только текст."
    )
    return await ask(prompt, [])
