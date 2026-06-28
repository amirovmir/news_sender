# news_sender Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Telegram-бот с ежедневной утренней рассылкой (7:00 UTC+3) — мотивация + погода + новости — и AI-чатом для нескольких пользователей.

**Architecture:** aiogram 3.x polling, PostgreSQL для хранения пользователей и истории диалогов, Redis для FSM, APScheduler с CronTrigger для утренних рассылок. Все внешние API бесплатные: Open-Meteo (погода), RSS-фиды (новости), Groq primary / Gemini fallback (AI).

**Tech Stack:** Python 3.11, aiogram 3.x, SQLAlchemy 2.0 async, asyncpg, alembic, APScheduler 3.x, aiohttp, feedparser, groq, google-generativeai, pydantic-settings, loguru, Docker Compose.

## Global Constraints

- Python 3.11+
- aiogram >= 3.10
- SQLAlchemy 2.0 с async engine (asyncpg драйвер)
- Все строки пользователю на русском языке
- HTML parse mode для всех сообщений Telegram
- Переменные окружения только через `.env` (никогда в коде)
- Логирование через loguru, не print/logging
- Все внешние API-вызовы обёрнуты в try/except с fallback или graceful degradation
- Файл `.env` в `.gitignore`

---

## File Map

```
news_sender/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Bot, Dispatcher, scheduler init, dp.start_polling
│   ├── config.py            # Pydantic Settings — все env переменные
│   ├── database.py          # async engine, AsyncSessionLocal, get_session, init_db
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── commands.py      # /start, /help, /weather, /news, /settings
│   │   ├── messages.py      # F.text catch-all → AI
│   │   └── callbacks.py     # inline кнопки настроек + FSM
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather.py       # get_weather_text(lat, lon, city_name) → str
│   │   ├── news.py          # get_news_summary() → str
│   │   ├── ai_service.py    # ask(question, history) → str
│   │   └── scheduler.py     # setup_scheduler(scheduler, bot), send_morning_digest
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User, ChatHistory SQLAlchemy Mapped models
│   └── keyboards/
│       ├── __init__.py
│       └── inline.py        # main_menu(), settings_menu()
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 0001_initial.py
├── deployments/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── alembic.ini
├── requirements.txt
└── .gitignore
```

---

### Task 1: Скелет проекта — config, requirements, Docker

**Files:**
- Create: `news_sender/requirements.txt`
- Create: `news_sender/bot/__init__.py`
- Create: `news_sender/bot/handlers/__init__.py`
- Create: `news_sender/bot/services/__init__.py`
- Create: `news_sender/bot/models/__init__.py`
- Create: `news_sender/bot/keyboards/__init__.py`
- Create: `news_sender/bot/config.py`
- Create: `news_sender/deployments/.env.example`
- Create: `news_sender/deployments/Dockerfile`
- Create: `news_sender/deployments/docker-compose.yml`
- Create: `news_sender/.gitignore`

**Interfaces:**
- Produces: `from bot.config import settings` — объект с полями ниже

- [ ] **Step 1: Создать `requirements.txt`**

```
aiogram==3.10.0
aiohttp==3.11.0
SQLAlchemy==2.0.36
asyncpg==0.30.0
alembic==1.14.0
redis==5.2.0
APScheduler==3.11.0
pydantic-settings==2.7.0
python-dotenv==1.0.1
loguru==0.7.3
groq==0.18.0
google-generativeai==0.8.0
feedparser==6.0.11
```

- [ ] **Step 2: Создать `bot/config.py`**

```python
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    bot_token: str
    admin_ids: List[int] = []

    groq_api_key: str
    gemini_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    gemini_model: str = "gemini-2.5-flash"

    database_url: str
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

- [ ] **Step 3: Создать `deployments/.env.example`**

```
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=[123456789]

GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql+asyncpg://botuser:botpassword@db:5432/botdb
REDIS_URL=redis://redis:6379/0

DB_PASSWORD=botpassword
```

- [ ] **Step 4: Создать `deployments/Dockerfile`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "bot.main"]
```

- [ ] **Step 5: Создать `deployments/docker-compose.yml`**

```yaml
version: '3.8'

services:
  bot:
    build:
      context: ..
      dockerfile: deployments/Dockerfile
    restart: always
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: botdb
      POSTGRES_USER: botuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U botuser -d botdb"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

- [ ] **Step 6: Создать `.gitignore`**

```
.env
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/
dist/
build/
.venv/
venv/
```

- [ ] **Step 7: Создать пустые `__init__.py`**

Создать пустые файлы:
- `bot/__init__.py`
- `bot/handlers/__init__.py`
- `bot/services/__init__.py`
- `bot/models/__init__.py`
- `bot/keyboards/__init__.py`

- [ ] **Step 8: Commit**

```bash
cd news_sender
git init
git add .
git commit -m "feat: project skeleton — config, requirements, Docker"
```

---

### Task 2: Модели БД + Alembic миграция

**Files:**
- Create: `news_sender/bot/models/user.py`
- Create: `news_sender/bot/database.py`
- Create: `news_sender/alembic.ini`
- Create: `news_sender/alembic/env.py`
- Create: `news_sender/alembic/versions/0001_initial.py`

**Interfaces:**
- Consumes: `from bot.config import settings` (settings.database_url)
- Produces:
  - `User` — SQLAlchemy модель с полями: telegram_id, username, city_name, city_lat, city_lon, notification_time, is_active, created_at
  - `ChatHistory` — SQLAlchemy модель с полями: user_id, role, content, created_at
  - `async_session_factory` — фабрика сессий
  - `get_session()` — async context manager
  - `init_db()` — создаёт таблицы (используется только в тестах; в prod — alembic)

- [ ] **Step 1: Создать `bot/models/user.py`**

```python
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100))
    city_name: Mapped[str] = mapped_column(String(100), default="Москва")
    city_lat: Mapped[float] = mapped_column(Float, default=55.7558)
    city_lon: Mapped[float] = mapped_column(Float, default=37.6173)
    notification_time: Mapped[str] = mapped_column(String(5), default="07:00")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    history: Mapped[list["ChatHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="history")
```

- [ ] **Step 2: Создать `bot/database.py`**

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from bot.config import settings
from bot.models.user import Base, User, ChatHistory
from loguru import logger

engine = create_async_engine(settings.database_url, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(telegram_id: int, username: str | None) -> User:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            await session.flush()
            await session.refresh(user)
        return user


async def get_user(telegram_id: int) -> User | None:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def update_user_city(telegram_id: int, city_name: str, lat: float, lon: float):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(city_name=city_name, city_lat=lat, city_lon=lon)
        )


async def update_user_time(telegram_id: int, notification_time: str):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(notification_time=notification_time)
        )


async def toggle_user_active(telegram_id: int, is_active: bool):
    async with get_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_active=is_active)
        )


async def get_all_active_users() -> list[User]:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.is_active == True))
        return list(result.scalars().all())


async def add_chat_message(telegram_id: int, role: str, content: str):
    async with get_session() as session:
        msg = ChatHistory(user_id=telegram_id, role=role, content=content)
        session.add(msg)


async def get_chat_history(telegram_id: int, limit: int = 10) -> list[ChatHistory]:
    async with get_session() as session:
        result = await session.execute(
            select(ChatHistory)
            .where(ChatHistory.user_id == telegram_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))
```

- [ ] **Step 3: Создать `alembic.ini`**

```ini
[alembic]
script_location = alembic
sqlalchemy.url = 

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

- [ ] **Step 4: Создать `alembic/env.py`**

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from bot.config import settings
from bot.models.user import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(conn=conn, target_metadata=target_metadata)
        )
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

- [ ] **Step 5: Создать `alembic/versions/0001_initial.py`**

```python
"""initial

Revision ID: 0001
Revises:
Create Date: 2026-06-29
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(100), nullable=True),
        sa.Column('city_name', sa.String(100), nullable=False, server_default='Москва'),
        sa.Column('city_lat', sa.Float(), nullable=False, server_default='55.7558'),
        sa.Column('city_lon', sa.Float(), nullable=False, server_default='37.6173'),
        sa.Column('notification_time', sa.String(5), nullable=False, server_default='07:00'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id'),
    )
    op.create_table(
        'chat_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.telegram_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_users_telegram_id', 'users', ['telegram_id'])
    op.create_index('idx_chat_history_user_id', 'chat_history', ['user_id'])


def downgrade():
    op.drop_table('chat_history')
    op.drop_table('users')
```

- [ ] **Step 6: Commit**

```bash
git add .
git commit -m "feat: DB models, database helpers, alembic migration"
```

---

### Task 3: Сервис погоды

**Files:**
- Create: `news_sender/bot/services/weather.py`

**Interfaces:**
- Consumes: ничего из других модулей
- Produces:
  - `get_weather_text(lat: float, lon: float, city_name: str) -> str` — HTML-строка с погодой
  - `geocode_city(city: str) -> tuple[float, float, str] | None` — (lat, lon, display_name)

- [ ] **Step 1: Создать `bot/services/weather.py`**

```python
import aiohttp
from loguru import logger

WEATHER_CODES = {
    0: "☀️ Ясно", 1: "🌤 Преим. ясно", 2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно", 45: "🌫 Туман", 48: "🌫 Изморозь",
    51: "🌦 Лёгкая морось", 61: "🌧 Небольшой дождь", 71: "🌨 Небольшой снег",
    80: "⛈ Ливень", 95: "⚡ Гроза",
}


async def geocode_city(city: str) -> tuple[float, float, str] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "ru", "format": "json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
        results = data.get("results")
        if not results:
            return None
        r = results[0]
        name = r.get("name", city)
        country = r.get("country", "")
        display = f"{name}, {country}" if country else name
        return r["latitude"], r["longitude"], display
    except Exception as e:
        logger.error(f"Geocode error for '{city}': {e}")
        return None


async def get_weather_text(lat: float, lon: float, city_name: str) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "Europe/Moscow",
        "forecast_days": 1,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()

        cur = data["current"]
        daily = data["daily"]
        code = cur.get("weather_code", 0)
        condition = WEATHER_CODES.get(code, "🌡")

        return (
            f"🌍 <b>{city_name}</b>\n"
            f"{condition} <b>{cur['temperature_2m']}°C</b> "
            f"(ощущается {cur['apparent_temperature']}°C)\n"
            f"💧 Влажность: {cur['relative_humidity_2m']}%\n"
            f"💨 Ветер: {cur['wind_speed_10m']} м/с\n"
            f"📊 Сегодня: макс {daily['temperature_2m_max'][0]}°C / "
            f"мин {daily['temperature_2m_min'][0]}°C, "
            f"осадки {daily['precipitation_sum'][0]} мм"
        )
    except Exception as e:
        logger.error(f"Weather error: {e}")
        return f"🌍 <b>{city_name}</b>\n⚠️ Погода временно недоступна"
```

- [ ] **Step 2: Проверить вручную (опционально)**

```python
# python -c "import asyncio; from bot.services.weather import get_weather_text; print(asyncio.run(get_weather_text(55.7558, 37.6173, 'Москва')))"
```

- [ ] **Step 3: Commit**

```bash
git add bot/services/weather.py
git commit -m "feat: weather service — Open-Meteo + geocoding"
```

---

### Task 4: Сервис новостей

**Files:**
- Create: `news_sender/bot/services/news.py`

**Interfaces:**
- Consumes: ничего из других модулей (AI суммаризация передаётся снаружи как callable)
- Produces:
  - `fetch_raw_headlines() -> list[str]` — список заголовков из RSS
  - `get_news_summary(summarize_fn) -> str` — HTML-строка; `summarize_fn(headlines: list[str]) -> str` — корутина

- [ ] **Step 1: Создать `bot/services/news.py`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add bot/services/news.py
git commit -m "feat: news service — RSS feeds + AI summarization interface"
```

---

### Task 5: AI сервис (Groq primary + Gemini fallback)

**Files:**
- Create: `news_sender/bot/services/ai_service.py`

**Interfaces:**
- Consumes: `from bot.config import settings`
- Produces:
  - `ask(question: str, history: list[dict]) -> str` — ответ AI
  - `generate_motivation() -> str` — мотивационная фраза
  - `summarize_headlines(headlines: list[str]) -> str` — сводка новостей (для news.py)

- [ ] **Step 1: Создать `bot/services/ai_service.py`**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add bot/services/ai_service.py
git commit -m "feat: AI service — Groq primary, Gemini fallback, motivation, news summary"
```

---

### Task 6: Клавиатуры и хендлеры команд

**Files:**
- Create: `news_sender/bot/keyboards/inline.py`
- Create: `news_sender/bot/handlers/commands.py`

**Interfaces:**
- Consumes:
  - `from bot.services.weather import get_weather_text`
  - `from bot.services.news import get_news_summary`
  - `from bot.services.ai_service import summarize_headlines`
  - `from bot.database import get_or_create_user, get_user`
- Produces: `router` (aiogram Router) для подключения в main.py

- [ ] **Step 1: Создать `bot/keyboards/inline.py`**

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌤 Погода", callback_data="weather"),
            InlineKeyboardButton(text="📰 Новости", callback_data="news"),
        ],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    ])


def settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏙 Изменить город", callback_data="set_city")],
        [InlineKeyboardButton(text="⏰ Изменить время уведомления", callback_data="set_time")],
        [InlineKeyboardButton(text="🔔 Вкл/Выкл уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
    ])
```

- [ ] **Step 2: Создать `bot/handlers/commands.py`**

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from bot.database import get_or_create_user, get_user
from bot.keyboards.inline import main_menu, settings_menu
from bot.services.weather import get_weather_text
from bot.services.news import get_news_summary
from bot.services.ai_service import summarize_headlines

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await get_or_create_user(message.from_user.id, message.from_user.username)
    text = (
        "👋 <b>Привет!</b>\n\n"
        "Я твой утренний помощник. Каждое утро в <b>7:00 по Москве</b> я пришлю:\n"
        "💪 Мотивацию на день\n"
        "🌤 Прогноз погоды\n"
        "📰 Краткую сводку главных новостей\n\n"
        "А ещё можешь просто написать мне — я отвечу с помощью AI!\n\n"
        "Настрой город и время в /settings"
    )
    await message.answer(text, reply_markup=main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📋 <b>Команды:</b>\n\n"
        "/start — приветствие и регистрация\n"
        "/weather — текущая погода\n"
        "/news — сводка новостей\n"
        "/settings — настройки (город, время, уведомления)\n"
        "/help — эта справка\n\n"
        "Или просто напиши что-нибудь — я отвечу!"
    )
    await message.answer(text)


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала напиши /start")
        return
    await message.answer("⏳ Запрашиваю погоду...")
    text = await get_weather_text(user.city_lat, user.city_lon, user.city_name)
    await message.answer(text)


@router.message(Command("news"))
async def cmd_news(message: Message):
    await message.answer("⏳ Собираю новости...")
    text = await get_news_summary(summarize_headlines)
    await message.answer(text)


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала напиши /start")
        return
    status = "✅ включены" if user.is_active else "❌ выключены"
    text = (
        f"⚙️ <b>Настройки</b>\n\n"
        f"🏙 Город: <b>{user.city_name}</b>\n"
        f"⏰ Время уведомлений: <b>{user.notification_time} (МСК)</b>\n"
        f"🔔 Уведомления: <b>{status}</b>"
    )
    await message.answer(text, reply_markup=settings_menu())
```

- [ ] **Step 3: Commit**

```bash
git add bot/keyboards/inline.py bot/handlers/commands.py
git commit -m "feat: keyboards and command handlers"
```

---

### Task 7: Callback-хендлеры и FSM настроек

**Files:**
- Create: `news_sender/bot/handlers/callbacks.py`

**Interfaces:**
- Consumes:
  - `from bot.database import get_user, update_user_city, update_user_time, toggle_user_active`
  - `from bot.services.weather import geocode_city, get_weather_text`
  - `from bot.keyboards.inline import main_menu, settings_menu`
- Produces: `router` (aiogram Router) с FSM SettingsState

- [ ] **Step 1: Создать `bot/handlers/callbacks.py`**

```python
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger

from bot.database import get_user, update_user_city, update_user_time, toggle_user_active
from bot.keyboards.inline import main_menu, settings_menu
from bot.services.weather import geocode_city, get_weather_text
from bot.services.news import get_news_summary
from bot.services.ai_service import summarize_headlines

router = Router()


class SettingsState(StatesGroup):
    waiting_city = State()
    waiting_time = State()


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery):
    await call.message.edit_text("Главное меню:", reply_markup=main_menu())


@router.callback_query(F.data == "weather")
async def cb_weather(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        await call.message.answer("Сначала напиши /start")
        return
    text = await get_weather_text(user.city_lat, user.city_lon, user.city_name)
    await call.message.answer(text)


@router.callback_query(F.data == "news")
async def cb_news(call: CallbackQuery):
    await call.answer()
    await call.message.answer("⏳ Собираю новости...")
    text = await get_news_summary(summarize_headlines)
    await call.message.answer(text)


@router.callback_query(F.data == "settings")
async def cb_settings(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        await call.message.answer("Сначала напиши /start")
        return
    status = "✅ включены" if user.is_active else "❌ выключены"
    text = (
        f"⚙️ <b>Настройки</b>\n\n"
        f"🏙 Город: <b>{user.city_name}</b>\n"
        f"⏰ Время: <b>{user.notification_time} (МСК)</b>\n"
        f"🔔 Уведомления: <b>{status}</b>"
    )
    await call.message.edit_text(text, reply_markup=settings_menu())


@router.callback_query(F.data == "set_city")
async def cb_set_city(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("🏙 Напиши название города (например: Москва, Казань, Новосибирск):")
    await state.set_state(SettingsState.waiting_city)


@router.message(SettingsState.waiting_city)
async def process_city(message: Message, state: FSMContext):
    await state.clear()
    result = await geocode_city(message.text.strip())
    if result is None:
        await message.answer("❌ Город не найден. Попробуй ещё раз: /settings")
        return
    lat, lon, display_name = result
    await update_user_city(message.from_user.id, display_name, lat, lon)
    weather = await get_weather_text(lat, lon, display_name)
    await message.answer(
        f"✅ Город изменён на <b>{display_name}</b>\n\n{weather}",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "set_time")
async def cb_set_time(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        "⏰ Введи время уведомлений в формате <b>ЧЧ:ММ</b> по московскому времени (МСК).\n"
        "Например: <code>07:00</code>, <code>08:30</code>"
    )
    await state.set_state(SettingsState.waiting_time)


@router.message(SettingsState.waiting_time)
async def process_time(message: Message, state: FSMContext):
    time_str = message.text.strip()
    try:
        parts = time_str.split(":")
        assert len(parts) == 2
        h, m = int(parts[0]), int(parts[1])
        assert 0 <= h <= 23 and 0 <= m <= 59
        formatted = f"{h:02d}:{m:02d}"
    except Exception:
        await message.answer("❌ Неверный формат. Введи время в формате ЧЧ:ММ, например: <code>07:00</code>")
        return
    await state.clear()
    await update_user_time(message.from_user.id, formatted)
    await message.answer(
        f"✅ Время уведомлений изменено на <b>{formatted} МСК</b>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "toggle_notifications")
async def cb_toggle(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    if not user:
        return
    new_state = not user.is_active
    await toggle_user_active(call.from_user.id, new_state)
    status = "✅ включены" if new_state else "❌ выключены"
    await call.message.answer(f"🔔 Уведомления теперь <b>{status}</b>")
```

- [ ] **Step 2: Commit**

```bash
git add bot/handlers/callbacks.py
git commit -m "feat: callback handlers and FSM settings (city, time, toggle)"
```

---

### Task 8: Хендлер сообщений (AI-чат)

**Files:**
- Create: `news_sender/bot/handlers/messages.py`

**Interfaces:**
- Consumes:
  - `from bot.services.ai_service import ask`
  - `from bot.database import get_chat_history, add_chat_message`
- Produces: `router` (aiogram Router)

- [ ] **Step 1: Создать `bot/handlers/messages.py`**

```python
from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from bot.services.ai_service import ask
from bot.database import get_chat_history, add_chat_message

router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    await message.bot.send_chat_action(message.chat.id, "typing")

    history_records = await get_chat_history(message.from_user.id, limit=10)
    history = [{"role": r.role, "content": r.content} for r in history_records]

    answer = await ask(message.text, history)

    await add_chat_message(message.from_user.id, "user", message.text)
    await add_chat_message(message.from_user.id, "assistant", answer)

    await message.answer(answer)
```

- [ ] **Step 2: Commit**

```bash
git add bot/handlers/messages.py
git commit -m "feat: message handler — AI chat with history"
```

---

### Task 9: Планировщик утренних рассылок

**Files:**
- Create: `news_sender/bot/services/scheduler.py`

**Interfaces:**
- Consumes:
  - `from bot.database import get_all_active_users`
  - `from bot.services.weather import get_weather_text`
  - `from bot.services.news import get_news_summary`
  - `from bot.services.ai_service import generate_motivation, summarize_headlines`
- Produces:
  - `setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot)` — регистрирует jobs
  - `reschedule_user(scheduler, bot, user)` — вызывается при изменении настроек

- [ ] **Step 1: Создать `bot/services/scheduler.py`**

```python
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from loguru import logger

from bot.database import get_all_active_users
from bot.services.weather import get_weather_text
from bot.services.news import get_news_summary
from bot.services.ai_service import generate_motivation, summarize_headlines


async def send_morning_digest(bot: Bot, telegram_id: int, city_lat: float,
                               city_lon: float, city_name: str):
    try:
        motivation = await generate_motivation()
        weather = await get_weather_text(city_lat, city_lon, city_name)
        news = await get_news_summary(summarize_headlines)

        sep = "━" * 28
        text = (
            f"🌅 <b>Доброе утро!</b>\n\n"
            f"💪 {motivation}\n\n"
            f"{sep}\n\n"
            f"{weather}\n\n"
            f"{sep}\n\n"
            f"{news}\n\n"
            f"{sep}\n"
            f"💬 Напиши мне что-нибудь — я отвечу!"
        )
        await bot.send_message(telegram_id, text)
        logger.info(f"Morning digest sent to {telegram_id}")
    except Exception as e:
        logger.error(f"Failed to send digest to {telegram_id}: {e}")


def _parse_time(notification_time: str) -> tuple[int, int]:
    parts = notification_time.split(":")
    return int(parts[0]), int(parts[1])


def reschedule_user(scheduler: AsyncIOScheduler, bot: Bot, telegram_id: int,
                    notification_time: str, city_lat: float, city_lon: float,
                    city_name: str, is_active: bool):
    job_id = f"morning_{telegram_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    if not is_active:
        return
    hour, minute = _parse_time(notification_time)
    scheduler.add_job(
        send_morning_digest,
        trigger=CronTrigger(hour=hour, minute=minute, timezone="Europe/Moscow"),
        args=[bot, telegram_id, city_lat, city_lon, city_name],
        id=job_id,
        replace_existing=True,
    )


async def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot):
    users = await get_all_active_users()
    for user in users:
        reschedule_user(
            scheduler, bot,
            user.telegram_id, user.notification_time,
            user.city_lat, user.city_lon, user.city_name,
            user.is_active,
        )
    logger.info(f"Scheduler set up for {len(users)} active users")
```

- [ ] **Step 2: Commit**

```bash
git add bot/services/scheduler.py
git commit -m "feat: APScheduler — morning digest per user at configured time"
```

---

### Task 10: Точка входа main.py + финальный деплой

**Files:**
- Create: `news_sender/bot/main.py`

**Interfaces:**
- Consumes: все handlers.router, services.scheduler, database.init_db, config.settings

- [ ] **Step 1: Создать `bot/main.py`**

```python
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from bot.config import settings
from bot.database import init_db
from bot.handlers import commands, messages, callbacks
from bot.services.scheduler import setup_scheduler


async def main():
    logger.info("Starting bot...")

    await init_db()

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
```

- [ ] **Step 2: Убедиться что `.env` создан из `.env.example` на VPS**

На VPS:
```bash
cd news_sender/deployments
cp .env.example .env
nano .env   # вставить BOT_TOKEN, GROQ_API_KEY, GEMINI_API_KEY, DB_PASSWORD
```

- [ ] **Step 3: Запустить через Docker Compose**

```bash
cd news_sender/deployments
docker compose up -d --build

# Проверить логи
docker compose logs -f bot
# Ожидаем: "Bot is running!"
```

- [ ] **Step 4: Запустить Alembic миграции**

```bash
docker compose exec bot alembic upgrade head
```

- [ ] **Step 5: Smoke test**
  1. Написать боту `/start` — должен ответить с клавиатурой
  2. Написать `/weather` — прогноз для Москвы
  3. Написать `/news` — сводка новостей
  4. Написать `/settings` → "Изменить город" → "Казань" — бот запрашивает, сохраняет, показывает погоду
  5. Написать произвольный вопрос — AI отвечает
  6. Дождаться 7:00 МСК (или временно изменить время через /settings) — проверить рассылку

- [ ] **Step 6: Финальный commit**

```bash
git add bot/main.py
git commit -m "feat: main entry point — bot startup, scheduler init, polling"
```

---

## Проверка покрытия спека

| Требование из спека | Task |
|---|---|
| Утреннее сообщение в 7:00 UTC+3 | Task 9 (CronTrigger Europe/Moscow 07:00) |
| Мотивационное сообщение | Task 5 (generate_motivation) |
| Прогноз погоды с выбором города | Task 3, Task 7 (FSM set_city) |
| Сводка новостей (RU + мировые) | Task 4 (RSS + Google News) |
| AI-чат с историей | Task 5, Task 8 |
| Несколько пользователей | Task 2 (users table), Task 9 (per-user jobs) |
| PostgreSQL + Redis + APScheduler | Task 1, Task 2, Task 9, Task 10 |
| Docker Compose деплой на VPS | Task 1, Task 10 |
| Groq primary + Gemini fallback | Task 5 |
| /settings FSM (город, время, toggle) | Task 7 |
| Graceful degradation при недоступных API | Task 3, 4, 5 (try/except) |
