# Telegram-бот с утренними уведомлениями и AI-ответами
## Полный технический анализ и руководство по реализации

**Дата:** 29 июня 2026 г.

---

## Содержание

1. [Обзор проекта](#1-обзор-проекта)
2. [API погоды](#2-api-погоды)
3. [API новостей](#3-api-новостей)
4. [AI API для ответов на вопросы](#4-ai-api-для-ответов-на-вопросы)
5. [Технологический стек](#5-технологический-стек)
6. [Архитектура бота](#6-архитектура-бота)
7. [Пример реализации](#7-пример-реализации)
8. [Деплой и эксплуатация](#8-деплой-и-эксплуатация)
9. [Бюджет и затраты](#9-бюджет-и-затраты)
10. [Рекомендации](#10-рекомендации)

---

## 1. Обзор проекта

### 1.1 Цель

Создание Telegram-бота, который:
- Каждое утро присылает персонализированные уведомления с прогнозом погоды и краткой сводкой новостей
- Отвечает на вопросы пользователей с помощью AI
- Работает 24/7 с минимальными затратами (преимущественно на бесплатных API)

### 1.2 Функциональные требования

| Функция | Описание | Приоритет |
|---------|----------|-----------|
| Утренние уведомления | Прогноз погоды + сводка новостей в заданное время | Обязательно |
| AI-ответы | Ответы на произвольные вопросы через AI API | Обязательно |
| Настройка времени | Пользователь выбирает время уведомлений | Обязательно |
| Выбор города | Пользователь указывает город для погоды | Обязательно |
| Категории новостей | Выбор тем (технологии, экономика, спорт и т.д.) | Желательно |
| История диалогов | Сохранение контекста разговора с AI | Желательно |
| Мультиязычность | Поддержка русского и английского языков | Желательно |

### 1.3 Нефункциональные требования

- **Экономичность:** Минимальные затраты (бесплатные API)
- **Надежность:** 99%+ аптайм, обработка ошибок, retry-логика
- **Масштабируемость:** Возможность роста до 1000+ пользователей
- **Безопасность:** Хранение ключей в .env, rate limiting, защита от спама

---

## 2. API погоды

### 2.1 Сравнительная таблица

| API | Бесплатный лимит | Без ключа | Покрытие РФ | Прогноз дней | Рейтинг |
|-----|-----------------|-----------|-------------|--------------|---------|
| **Open-Meteo** | 10 000/день | Да | Да | 16 | ★★★★★ |
| **OpenWeatherMap** | 1 000 000/мес | Нет | Да | 5 (3ч) | ★★★★☆ |
| **WeatherAPI.com** | 1 млн/мес | Нет | Да | 14 | ★★★★☆ |
| **Yandex.Weather** | 50/день (пост.) / 5000/день (30 дн) | Нет | **Отличное** | 7 | ★★★★☆ |
| **Visual Crossing** | 1 000/день | Нет | Да | 15 | ★★★★☆ |
| **Tomorrow.io** | 500/день | Нет | Да | 14 | ★★★★☆ |
| **PirateWeather** | 10 000/мес | Нет | Да | 7 | ★★★★☆ |
| **Weatherbit** | 50/день | Нет | Да | 16 | ★★★☆☆ |
| **Weatherstack** | 100/мес | Нет | Да | 14 (платно) | ★★☆☆☆ |

### 2.2 Рекомендуемое решение

**Стратегия: Primary + Fallback + Emergency**

| Приоритет | API | Причина выбора |
|-----------|-----|---------------|
| **Primary** | Open-Meteo | Без ключа, 10K/день, отличное покрытие |
| **Fallback** | OpenWeatherMap | 1M/мес, русский язык, надежность |
| **Для РФ** | Yandex.Weather | Лучшая точность для России (50/день) |
| **Emergency** | 7Timer | Без ключа, без лимитов, простой формат |

### 2.3 Пример кода: Open-Meteo

```python
import aiohttp
import asyncio

async def get_weather_open_meteo(city_lat: float = 55.7558, 
                                  city_lon: float = 37.6173) -> dict:
    """Open-Meteo API — не требует API-ключа"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_lat,
        "longitude": city_lon,
        "current": "temperature_2m,relative_humidity_2m,"
                   "weather_code,wind_speed_10m,apparent_temperature",
        "daily": "temperature_2m_max,temperature_2m_min,"
                 "precipitation_sum,weather_code",
        "timezone": "auto",
        "forecast_days": 3
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            
    current = data.get("current", {})
    daily = data.get("daily", {})
    
    # Расшифровка weather_code в текст
    weather_codes = {
        0: "Ясно", 1: "Преимущественно ясно", 2: "Переменная облачность",
        3: "Пасмурно", 45: "Туман", 48: "Изморозь",
        51: "Лёгкая морось", 61: "Небольшой дождь", 71: "Небольшой снег",
        80: "Ливневые дожди", 95: "Гроза"
    }
    
    code = current.get("weather_code", 0)
    
    return {
        "temp": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind": current.get("wind_speed_10m"),
        "condition": weather_codes.get(code, "Неизвестно"),
        "forecast": [
            {
                "max": daily["temperature_2m_max"][i] if "temperature_2m_max" in daily else None,
                "min": daily["temperature_2m_min"][i] if "temperature_2m_min" in daily else None,
            }
            for i in range(min(3, len(daily.get("time", []))))
        ]
    }
```

---

## 3. API новостей

### 3.1 Сравнительная таблица

| API | Бесплатный лимит | Русский язык | Источники | Задержка | Рейтинг |
|-----|-----------------|--------------|-----------|----------|---------|
| **Currents API** | 1 000/день | Да (20+ языков) | 120 000+ | Реальное время | ★★★★★ |
| **NewsAPI.org** | 100/день | Да (14 языков) | 150 000+ | 24 часа | ★★★☆☆ |
| **GNews API** | 100/день | Да (41 язык) | 80 000+ | Реальное время | ★★★★☆ |
| **NewsData.io** | 200 кредитов/день | Да (89 языков) | 97 000+ | 12 часов | ★★★★☆ |
| **RSS-фиды** | Без лимитов | Да (полный контент) | Любые | Реальное время | ★★★★★ |

### 3.2 Рекомендуемое решение

**Стратегия: RSS-фиды (основной) + Currents API (резерв)**

RSS-фиды являются оптимальным выбором для русскоязычных новостей:
- Полностью бесплатно, без лимитов
- Прямой доступ к российским СМИ
- Полный контент на русском языке
- Реальное время обновлений

**Основные RSS-источники:**

| Источник | URL |
|----------|-----|
| РИА Новости | https://ria.ru/export/rss2/index.xml |
| ТАСС | https://tass.ru/rss/v2.xml |
| Лента.ру | https://lenta.ru/rss/news |
| РБК | https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss |
| Коммерсант | https://www.kommersant.ru/RSS/news.xml |
| Ведомости | https://www.vedomosti.ru/rss/news |
| Google News RU | https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru |

### 3.3 Пример кода: RSS + AI-суммаризация

```python
import aiohttp
import feedparser
from typing import List, Dict

RSS_FEEDS = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
}

async def fetch_rss_feed(session: aiohttp.ClientSession, 
                         name: str, url: str, limit: int = 3) -> List[Dict]:
    """Получение новостей из RSS-ленты"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            content = await resp.text()
            feed = feedparser.parse(content)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": name
                })
            return articles
    except Exception as e:
        print(f"Ошибка при получении {name}: {e}")
        return []

async def get_all_news() -> List[Dict]:
    """Получение новостей со всех источников"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_rss_feed(session, name, url)
            for name, url in RSS_FEEDS.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_news = []
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
        
        # Удаление дубликатов по заголовку
        seen = set()
        unique = []
        for article in all_news:
            if article["title"] not in seen:
                seen.add(article["title"])
                unique.append(article)
        
        return unique[:15]  # Топ-15 новостей
```

---

## 4. AI API для ответов на вопросы

### 4.1 Сравнительная таблица

| API | Бесплатно | Лимиты | Лучшие модели | Русский язык | Рейтинг |
|-----|-----------|--------|---------------|-------------|---------|
| **OpenRouter** | ✅ 27+ моделей | 20 RPM, 50-200 RPD | Llama 4, Qwen3, DeepSeek | ⭐⭐⭐⭐ | ★★★★★ |
| **Groq API** | ✅ | 30 RPM, 1K-14.4K RPD | Llama 4 Scout, Qwen3 | ⭐⭐⭐⭐ | ★★★★★ |
| **DeepSeek API** | ✅ 5M токенов (30 дн.) | 30 дней | V4 Flash, R1 | ⭐⭐⭐⭐⭐ | ★★★★★ |
| **Google Gemini** | ✅ ~1 500/день | 10 RPM | 2.5 Flash, Flash-Lite | ⭐⭐⭐⭐ | ★★★★☆ |
| **Kimi API (Moonshot)** | ❌ (мин. $1) | Зависит от баланса | K2.5, K2.6 | ⭐⭐⭐⭐⭐ | ★★★★☆ |
| **Cerebras** | ✅ 1M токенов/день | 5 RPM | GPT-OSS-120B, Qwen3 | ⭐⭐⭐⭐ | ★★★★★ |
| **GitHub Models** | ✅ | 10 RPM, 50-150 RPD | GPT-5, Llama 4 | ⅈ⭐⭐⭐⭐⭐ | ★★★★☆ |
| **Ollama (локально)** | ✅ Полностью | Безлимитно | Любые GGUF | ⭐⭐⭐⭐ | ★★★★☆ |

### 4.2 Рекомендуемое решение

**Стратегия: Бесплатный тир с fallback-цепочкой**

| Приоритет | API | Модель | Причина |
|-----------|-----|--------|---------|
| **1** | Groq API | `llama-3.3-70b-versatile` | Быстрый, 1000 RPD, без карты |
| **2** | OpenRouter | `deepseek/deepseek-r1:free` | Reasoning, отличный русский |
| **3** | Google Gemini | `gemini-2.5-flash` | 1500/день, надежный |
| **4 (локально)** | Ollama | `qwen3:14b` | Полная приватность, бесплатно |

**По поводу Kimi API:** У Moonshot AI нет постоянного бесплатного тарифа. Требуется минимум $1 для активации. Зато это отличный вариант по цене: $0.60/M input токенов, 256K контекст, отличное качество на русском языке.

### 4.3 Пример кода: Groq API (бесплатно)

```python
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def ask_ai(question: str, context: str = "") -> str:
    """Ответ на вопрос через Groq API (бесплатно)"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Ты — дружелюбный ассистент в Telegram-боте. "
                        "Отвечай кратко и по делу на русском языке. "
                        "Используй форматирование Markdown где уместно."
                    )
                },
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Извините, произошла ошибка: {str(e)}"
```

### 4.4 Пример кода: OpenRouter (бесплатные модели)

```python
import aiohttp
import os

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

async def ask_openrouter(question: str) -> str:
    """Ответ через OpenRouter с бесплатной моделью"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/your_bot",
        "X-Title": "Telegram Morning Bot"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "Отвечай на русском языке. Будь кратким и полезным."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
```

---

## 5. Технологический стек

### 5.1 Рекомендуемый стек

| Компонент | Технология | Альтернатива |
|-----------|-----------|--------------|
| **Фреймворк** | aiogram 3.x | python-telegram-bot 22.x |
| **База данных** | PostgreSQL | SQLite (для старта) |
| **Кэш / FSM** | Redis | MemoryStorage (только dev) |
| **ORM** | SQLAlchemy 2.0 | Tortoise ORM |
| **Планировщик** | APScheduler | PTB JobQueue |
| **HTTP-клиент** | aiohttp | httpx |
| **Логирование** | loguru | structlog |
| **Конфигурация** | Pydantic Settings | python-dotenv |
| **Мониторинг** | UptimeRobot + Sentry | Grafana + Prometheus |

### 5.2 Почему aiogram 3.x

- **Современная архитектура:** Система Routers для модульности
- **FSM:** Встроенная машина состояний для многошаговых диалогов
- **Magic Filters:** Декларативные фильтры
- **Полная асинхронность:** Нативная поддержка asyncio
- **Хранилище:** Гибкая система (Memory, Redis, MongoDB)

### 5.3 Почему APScheduler

- **CronTrigger:** Точное время уведомлений
- **AsyncIOScheduler:** Интеграция с asyncio
- **Job stores:** Хранение задач в PostgreSQL/Redis
- **Фоновое выполнение:** Не блокирует event loop

---

## 6. Архитектура бота

### 6.1 Структура проекта

```
telegram-morning-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py            # Pydantic Settings
│   ├── constants.py         # Константы
│   ├── handlers/
│   │   ├── commands.py      # /start, /help, /settings
│   │   ├── messages.py      # Обработка сообщений
│   │   └── callbacks.py     # Callback-кнопки
│   ├── services/
│   │   ├── weather.py       # API погоды
│   │   ├── news.py          # API новостей
│   │   ├── ai_service.py    # AI-ответы
│   │   └── scheduler.py     # Утренние уведомления
│   ├── models/
│   │   └── user.py          # SQLAlchemy модели
│   ├── keyboards/
│   │   └── inline.py        # Клавиатуры
│   └── utils/
│       └── retry.py         # Retry-логика
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── .gitignore
```

### 6.2 Архитектурная схема

```
                    +------------------+
                    |   Telegram API   |
                    +--------+---------+
                             |
                    +--------v---------+
                    |  aiogram 3.x Bot |
                    |  +-------------+ |
                    |  |  Handlers   | |
                    |  |   Routers   | |
                    |  +-------------+ |
                    |  +-------------+ |
                    |  |  FSM        | |
                    |  | (настройки) | |
                    |  +-------------+ |
                    +--------+---------+
                             |
          +------------------+------------------+
          |                  |                  |
+---------v------+  +--------v-------+  +-------v--------+
| WeatherService |  |  NewsService   |  |  AIService     |
| (Open-Meteo)   |  |  (RSS-фиды)    |  |  (Groq API)    |
+--------+-------+  +--------+-------+  +-------+--------+
         |                   |                  |
         +-------------------+------------------+
                             |
                    +--------v---------+
                    |   Data Layer     |
                    |  +-------------+ |
                    |  | PostgreSQL  | |
                    |  |   (users)   | |
                    |  +-------------+ |
                    |  +-------------+ |
                    |  |    Redis    | |
                    |  | (cache/FSM) | |
                    |  +-------------+ |
                    |  +-------------+ |
                    |  | APScheduler | |
                    |  |  (задачи)   | |
                    |  +-------------+ |
                    +------------------+
```

### 6.3 База данных

```sql
-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    city VARCHAR(100) DEFAULT 'Moscow',
    city_lat FLOAT DEFAULT 55.7558,
    city_lon FLOAT DEFAULT 37.6173,
    notification_time VARCHAR(5) DEFAULT '08:00',
    timezone VARCHAR(50) DEFAULT 'Europe/Moscow',
    news_categories JSONB DEFAULT '["general"]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- История сообщений (для контекста AI)
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id),
    role VARCHAR(20) NOT NULL,  -- 'user' или 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
```

---

## 7. Пример реализации

### 7.1 requirements.txt

```
# Core
aiogram==3.28.0
aiohttp==3.11.0

# Database
SQLAlchemy==2.0.36
asyncpg==0.30.0
alembic==1.14.0
redis==5.2.0

# Scheduler
APScheduler==3.11.0

# Configuration
pydantic==2.10.0
pydantic-settings==2.7.0
python-dotenv==1.0.1

# Logging
loguru==0.7.3

# AI
groq==0.18.0
openai==1.60.0

# News parsing
feedparser==6.0.11

# Monitoring
sentry-sdk==2.19.0
```

### 7.2 Конфигурация (config.py)

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Telegram
    bot_token: str
    admin_ids: List[int] = []
    
    # AI API (Groq — бесплатно)
    groq_api_key: str
    ai_model: str = "llama-3.3-70b-versatile"
    
    # Weather (не требует ключа для Open-Meteo)
    openweather_api_key: str = ""  # Fallback
    
    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost/botdb"
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 7.3 Главный файл (main.py)

```python
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from bot.config import settings
from bot.handlers import commands, messages
from bot.services.scheduler import setup_scheduler
from bot.database import init_db

async def main():
    # Инициализация БД
    await init_db()
    
    # Redis storage для FSM
    storage = RedisStorage.from_url(settings.redis_url)
    
    # Bot + Dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    
    # Подключение роутеров
    dp.include_router(commands.router)
    dp.include_router(messages.router)
    
    # Планировщик утренних уведомлений
    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot)
    scheduler.start()
    
    logger.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 7.4 Обработчики команд (handlers/commands.py)

```python
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.services.weather import get_weather_text
from bot.services.news import get_news_text
from bot.services.ai_service import ask_ai
from bot.keyboards.inline import main_menu, settings_menu

router = Router()

class SettingsState(StatesGroup):
    waiting_city = State()
    waiting_time = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "👋 <b>Привет!</b>\n\n"
        "Я ваш утренний помощник. Каждое утро я присылаю:\n"
        "🌤 Прогноз погоды\n"
        "📰 Сводку главных новостей\n\n"
        "А ещё я могу ответить на любой вопрос с помощью AI!\n\n"
        "Настройте время и город в /settings"
    )
    await message.answer(welcome_text, reply_markup=main_menu())

@router.message(Command("weather"))
async def cmd_weather(message: Message):
    """Текущая погода"""
    weather = await get_weather_text(message.from_user.id)
    await message.answer(weather)

@router.message(Command("news"))
async def cmd_news(message: Message):
    """Сводка новостей"""
    news = await get_news_text()
    await message.answer(news, disable_web_page_preview=True)

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Настройки"""
    await message.answer("⚙️ Настройки:", reply_markup=settings_menu())
```

### 7.5 Обработчик AI-вопросов (handlers/messages.py)

```python
from aiogram import Router, F
from aiogram.types import Message
from bot.services.ai_service import ask_ai

router = Router()

@router.message(F.text)
async def handle_message(message: Message):
    """Все текстовые сообщения обрабатываются как вопросы к AI"""
    # Показываем, что бот "печатает"
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем ответ от AI
    answer = await ask_ai(message.text)
    
    await message.answer(answer)
```

### 7.6 Сервис погоды (services/weather.py)

```python
import aiohttp
from bot.database import get_user_city

WEATHER_CODES = {
    0: "☀️ Ясно", 1: "🌤 Преимущественно ясно", 
    2: "⛅ Переменная облачность", 3: "☁️ Пасмурно",
    45: "🌫 Туман", 48: "🌫 Изморозь",
    51: "🌦 Лёгкая морось", 61: "🌧 Небольшой дождь",
    71: "🌨 Небольшой снег", 80: "⛈ Ливневые дожди",
    95: "⚡ Гроза"
}

async def get_weather_text(user_id: int) -> str:
    """Формирование текстового прогноза погоды"""
    city_data = await get_user_city(user_id)
    lat, lon = city_data["lat"], city_data["lon"]
    city_name = city_data["name"]
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,apparent_temperature,"
                   "relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto", "forecast_days": 1
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
    
    current = data["current"]
    daily = data["daily"]
    
    weather_code = current.get("weather_code", 0)
    condition = WEATHER_CODES.get(weather_code, "🌡")
    
    return (
        f"🌍 <b>{city_name}</b>\n\n"
        f"{condition} <b>{current['temperature_2m']}°C</b> "
        f"(ощущается как {current['apparent_temperature']}°C)\n"
        f"💧 Влажность: {current['relative_humidity_2m']}%\n"
        f"💨 Ветер: {current['wind_speed_10m']} м/с\n\n"
        f"📊 <b>Сегодня:</b>\n"
        f"🌡 Макс: {daily['temperature_2m_max'][0]}°C | "
        f"Мин: {daily['temperature_2m_min'][0]}°C\n"
        f"🌧 Осадки: {daily['precipitation_sum'][0]} мм"
    )
```

### 7.7 Сервис новостей (services/news.py)

```python
import aiohttp
import feedparser
import asyncio
from typing import List, Dict

RSS_FEEDS = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
}

async def fetch_feed(session: aiohttp.ClientSession, 
                     name: str, url: str, limit: int = 3) -> List[Dict]:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            feed = feedparser.parse(await resp.text())
            return [
                {"title": e.get("title", ""), "link": e.get("link", ""), 
                 "source": name}
                for e in feed.entries[:limit]
            ]
    except Exception:
        return []

async def get_news_text() -> str:
    """Формирование сводки новостей"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, name, url) 
                for name, url in RSS_FEEDS.items()]
        results = await asyncio.gather(*tasks)
    
    all_news = []
    for result in results:
        all_news.extend(result)
    
    # Уникальные заголовки
    seen = set()
    unique = []
    for n in all_news:
        if n["title"] not in seen:
            seen.add(n["title"])
            unique.append(n)
    
    # Формируем текст
    text = "📰 <b>Главные новости</b>\n\n"
    for i, article in enumerate(unique[:10], 1):
        text += f"{i}. {article['title']}\n"
        text += f"   <i>Источник: {article['source']}</i>\n\n"
    
    return text
```

### 7.8 Сервис AI (services/ai_service.py)

```python
from groq import Groq
from bot.config import settings

client = Groq(api_key=settings.groq_api_key)

async def ask_ai(question: str) -> str:
    """Ответ на вопрос через Groq API (Llama 3.3 — бесплатно)"""
    try:
        response = client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — интеллектуальный ассистент в Telegram. "
                        "Отвечай на русском языке. Будь кратким, но информативным. "
                        "Используй HTML-форматирование: <b>жирный</b>, <i>курсив</i>."
                    )
                },
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Ошибка при обращении к AI: {str(e)}\nПопробуйте позже."
```

### 7.9 Планировщик уведомлений (services/scheduler.py)

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from loguru import logger

from bot.database import get_all_active_users
from bot.services.weather import get_weather_text
from bot.services.news import get_news_text

async def send_morning_notification(bot: Bot, user_id: int):
    """Отправка утреннего уведомления пользователю"""
    try:
        # Получаем погоду и новости
        weather = await get_weather_text(user_id)
        news = await get_news_text()
        
        # Формируем сообщение
        message = (
            f"🌅 <b>Доброе утро!</b>\n\n"
            f"{weather}\n\n"
            f"{'━' * 30}\n\n"
            f"{news}\n\n"
            f"💡 Задайте мне любой вопрос — я отвечу!"
        )
        
        await bot.send_message(user_id, message, 
                              disable_web_page_preview=True)
        logger.info(f"Утреннее уведомление отправлено: {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки {user_id}: {e}")

def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot):
    """Настройка планировщика утренних уведомлений"""
    # Загружаем пользователей и создаём задачи
    async def schedule_all_users():
        users = await get_all_active_users()
        for user in users:
            hour, minute = map(int, user["notification_time"].split(":"))
            scheduler.add_job(
                send_morning_notification,
                trigger=CronTrigger(hour=hour, minute=minute, 
                                   timezone=user["timezone"]),
                args=[bot, user["telegram_id"]],
                id=f"morning_{user['telegram_id']}",
                replace_existing=True,
            )
    
    # Запускаем первоначальное планирование
    import asyncio
    asyncio.create_task(schedule_all_users())
```

### 7.10 Клавиатуры (keyboards/inline.py)

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌤 Погода", callback_data="weather"),
         InlineKeyboardButton(text="📰 Новости", callback_data="news")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="❓ Задать вопрос AI", callback_data="ask_ai")]
    ])

def settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏙 Изменить город", callback_data="set_city")],
        [InlineKeyboardButton(text="⏰ Время уведомлений", callback_data="set_time")],
        [InlineKeyboardButton(text="🔔 Вкл/Выкл уведомления", 
                             callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
```

### 7.11 Docker-конфигурация

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Запуск
CMD ["python", "-m", "bot.main"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  bot:
    build: .
    restart: always
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: botdb
      POSTGRES_USER: botuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 8. Деплой и эксплуатация

### 8.1 Варианты хостинга

| Провайдер | Стоимость | Локация | Рекомендация |
|-----------|-----------|---------|--------------|
| **Hetzner** | ~4.51 EUR/мес | Германия | Лучшая цена |
| **DigitalOcean** | $5/мес | США/Европа | Простой старт |
| **Timeweb** | ~200 руб/мес | Россия | Соответствие 152-ФЗ |

**Важно:** Бесплатные хостинги (Render, Railway free tier) не подходят для ботов с уведомлениями по расписанию, так как они "засыпают" при отсутствии активности.

### 8.2 Запуск через Docker

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/telegram-morning-bot.git
cd telegram-morning-bot

# Создание .env файла
cp .env.example .env
# Отредактируйте .env, добавив свои ключи

# Запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot
```

### 8.3 Мониторинг

| Инструмент | Назначение | Стоимость |
|------------|-----------|-----------|
| **UptimeRobot** | Проверка доступности | Бесплатно |
| **Sentry** | Отслеживание ошибок | Бесплатно |
| **Healthchecks.io** | Проверка heartbeat | Бесплатно |

---

## 9. Бюджет и затраты

### 9.1 Минимальный бюджет (все API бесплатные)

| Компонент | Стоимость/мес |
|-----------|--------------|
| VPS (Hetzner CX11) | ~4.51 EUR (~$5) |
| Open-Meteo API | Бесплатно |
| RSS-фиды новостей | Бесплатно |
| Groq API (AI) | Бесплатно |
| UptimeRobot | Бесплатно |
| Sentry | Бесплатно |
| **ИТОГО** | **~$5/мес** |

### 9.2 Улучшенный вариант (с Kimi API)

| Компонент | Стоимость/мес |
|-----------|--------------|
| VPS (Hetzner) | ~$5 |
| Kimi API (~10K запросов) | ~$1-3 |
| **ИТОГО** | **~$6-8/мес** |

### 9.3 Масштабирование (1 000+ пользователей)

| Компонент | Стоимость/мес |
|-----------|--------------|
| VPS (Hetzner CPX21 — 4GB RAM) | ~$10 |
| AI API (Groq бесплатно / Kimi ~$5) | ~$5 |
| **ИТОГО** | **~$15/мес** |

---

## 10. Рекомендации

### 10.1 Порядок разработки

1. **Неделя 1 — MVP:**
   - aiogram 3.x + SQLite + MemoryStorage
   - Команды /start, /help, /weather, /news
   - Интеграция Open-Meteo + RSS
   - Ручной запрос погоды и новостей

2. **Неделя 2 — AI + уведомления:**
   - PostgreSQL + Redis + SQLAlchemy
   - Интеграция Groq API
   - APScheduler + утренние уведомления
   - Настройки пользователя (город, время)

3. **Неделя 3 — Production:**
   - Docker + деплой на VPS
   - Rate limiting + логирование
   - Мониторинг + алерты
   - Тестирование и отладка

### 10.2 Лучшие практики

- **Обработка ошибок:** Всегда используйте try/except для внешних API
- **Retry-логика:** 3 попытки с экспоненциальным backoff
- **Rate limiting:** Максимум 10-20 сообщений/минуту на пользователя
- **Логирование:** Используйте loguru для структурированных логов
- **Мониторинг:** Настройте UptimeRobot для проверки доступности

### 10.3 Безопасность

- Храните все API-ключи в `.env` (никогда в коде!)
- Добавьте `.env` в `.gitignore`
- Используйте rate limiting для защиты от спама
- При работе с пользователями из РФ учитывайте требования 152-ФЗ
- Минимизируйте сбор персональных данных

### 10.4 Возможные улучшения

- **Голосовые сообщения:** Интеграция Whisper для распознавания речи
- **Инлайн-режим:** Поиск погоды и новостей в любом чате
- **Статистика:** Аналитика использования через Grafana
- **A/B тестирование:** Тестирование разных AI-моделей
- **Мультиязычность:** Поддержка английского, китайского и других языков

---

## Заключение

Представленное решение позволяет создать полнофункционального Telegram-бота с минимальными затратами (~$5/мес). Благодаря использованию бесплатных API (Open-Meteo для погоды, RSS-фиды для новостей, Groq для AI) бот может обслуживать сотни пользователей без дополнительных расходов.

Ключевые преимущества архитектуры:
- **Модульность:** Легко заменять API и добавлять новые функции
- **Надежность:** Fallback-цепочки для всех внешних сервисов
- **Масштабируемость:** От 1 до 10 000+ пользователей
- **Безопасность:** Хранение данных на собственном сервере
