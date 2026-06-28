# Технологический стек для Telegram-бота с утренними уведомлениями и AI-ответами

> **Дата исследования:** Июль 2025
> **Актуальность:** 2025-2026 гг.
> **Задача:** Подбор оптимального стека для Telegram-бота с утренними уведомлениями (погода + новости), AI-ответами, хранением настроек пользователей и возможностью масштабирования.

---

## 1. Сравнение Python-фреймворков для Telegram-ботов

### 1.1 Обзор фреймворков

| Фреймворк | Версия (2025) | Протокол | Асинхронность | Статус |
|-----------|--------------|----------|---------------|--------|
| **aiogram** | 3.28.x | Bot API (HTTP) | Полная (asyncio) | Активно развивается |
| **python-telegram-bot (PTB)** | 22.x | Bot API (HTTP) | Полная (asyncio) | Активно развивается |
| **Telethon** | 1.44.x | MTProto (TCP) | Полная (asyncio) | Активно развивается |
| **Pyrogram** | 2.x | MTProto (TCP) | Полная (asyncio) | **Заброшен** (не поддерживается) |

### 1.2 Детальное сравнение

| Критерий | aiogram 3.x | PTB 22.x | Telethon | Pyrogram |
|----------|-------------|----------|----------|----------|
| **API покрытие** | Bot API 8.2 | Bot API 8.2 | Полный MTProto | MTProto (устаревший) |
| **Архитектура** | Router + Dispatcher | Application + Updater | Event-based Client | Client-based |
| **FSM** | Встроенный (states) | Через сторонние | Нет встроенного | Нет встроенного |
| **Фильтры** | Magic Filters | Базовые + кастомные | Events + filters | Декораторы |
| **Документация** | Отличная (docs.aiogram.dev) | Отличная (RTD) | Хорошая | Устаревшая |
| **Сообщество** | Большое (RU + EN) | Огромное (EN) | Среднее | Минимальное |
| **Middleware** | Встроенный | Встроенный | Встроенный | Встроенный |
| **Сложность входа** | Средняя | Низкая | Высокая | Средняя |
| **Webhook/Polling** | Оба | Оба + JobQueue | Только polling | Polling |
| **Рекомендация** | **Лучший выбор** | Отличная альтернатива | Userbot/продвинутые | **Не рекомендуется** |

### 1.3 Почему aiogram 3.x — лучший выбор

- **Современная архитектура:** Система Routers позволяет разбивать обработчики на модули — идеально для масштабирования
- **FSM (Finite State Machine):** Встроенная машина состояний для многошаговых диалогов (настройка уведомлений, опросы)
- **Magic Filters:** Декларативные фильтры (`F.text == "Привет"`, `F.from_user.id.in_(ADMINS)`)
- **Полная асинхронность:** Нативная поддержка asyncio, aiohttp под капотом
- **Storage:** Гибкая система хранения состояний — MemoryStorage (dev), RedisStorage (prod)
- **Aiogram-Dialog:** Отдельная библиотека для создания сложных диалоговых интерфейсов
- **Активное развитие:** Регулярные релизы, Bot API 8.2, поддержка Python 3.9+

### 1.4 Когда выбрать PTB (python-telegram-bot)

- Более простой вход для новичков
- Встроенный **JobQueue** для планировки задач (утренние уведомления)
- Огромное англоязычное сообщество
- Отличная документация на ReadTheDocs
- Версия 22.x: поддержка Bot API 8.2, улучшенная работа с датами

### 1.5 Telethon — когда нужен

- Доступ к **MTProto API** (не только Bot API)
- Userbot-функциональность (чтение каналов, личные сообщения)
- Более низкоуровневый контроль
- Требует `api_id` и `api_hash`
- Не рекомендуется для классических ботов — избыточная сложность

### 1.6 Pyrogram — не рекомендуется

> **Важно:** Pyrogram официально заброшен. На сайте docs.pyrogram.org указано: "The project is no longer maintained or supported."
> 
> Использовать только если нужна совместимость с legacy-кодом. Для новых проектов — aiogram 3.x.

---

## 2. Хранение данных

### 2.1 Сравнение баз данных

| Критерий | SQLite | PostgreSQL | Redis |
|----------|--------|------------|-------|
| **Архитектура** | Встроенная (файл) | Клиент-сервер | Ключ-значение (in-memory) |
| **Настройка** | Zero-config | Требует установки | Требует установки |
| **Конкурентность** | 1 writer | MVCC, полная | Однопоточная (event loop) |
| **Производительность** | Отличная для малых | Отличная для больших | Субмиллисекундная |
| **Типы данных** | Базовые | Расширенные (JSONB, массивы) | Строки, хеши, списки, сеты |
| **Репликация** | Нет | Streaming + logical | Sentinel, Cluster |
| **Бэкапы** | Копия файла | pg_dump, WAL | RDB + AOF |
| **Идеально для** | < 1000 пользователей | > 1000 пользователей, продакшн | Кэш, сессии, FSM |
| **Цена (VPS)** | Бесплатно | Бесплатно (self-hosted) | Бесплатно (self-hosted) |

### 2.2 Рекомендации по выбору

**Для небольшого бота (до 1000 пользователей):**
- **SQLite** — достаточно, zero-config, переносимость
- Можно комбинировать с **Redis** для FSM и кэша

**Для масштабируемого бота (1000+ пользователей):**
- **PostgreSQL** — основное хранилище
- **Redis** — для кэширования, FSM состояний, rate limiting
- Размещение на сервере в РФ (требование 152-ФЗ)

### 2.3 ORM для работы с базой данных

| ORM | Тип | Асинхронность | Поддержка БД | Рекомендация |
|-----|-----|---------------|--------------|--------------|
| **SQLAlchemy 2.0** | Полнофункциональный ORM | Native async (asyncio) | PostgreSQL, SQLite, MySQL | **Рекомендуется** |
| **Tortoise ORM** | Async-native ORM | Native async | PostgreSQL, SQLite, MySQL | Отличная альтернатива |
| **GINO** | Lightweight async ORM | Native async | PostgreSQL, MySQL | Устаревает |

**Рекомендация: SQLAlchemy 2.0**

- Стандарт де-факто в Python-экосистеме
- Полная поддержка асинхронности через `AsyncSession`, `create_async_engine`
- Мощная система миграций через **Alembic**
- Pydantic-интеграция через `sqlalchemy-to-pydantic`
- Пример использования с aiogram 3:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, TIMESTAMP, Integer, String, BigInteger, JSON

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(100))
    notification_time: Mapped[str] = mapped_column(String(5), default="08:00")  # HH:MM
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow")
    preferences: Mapped[dict] = mapped_column(JSON, default={})
    is_active: Mapped[bool] = mapped_column(default=True)
```

---

## 3. Планировщики задач

### 3.1 Сравнение подходов для утренних уведомлений

| Планировщик | Тип | Сложность | Надежность | Масштабирование | Рекомендация |
|-------------|-----|-----------|------------|-----------------|--------------|
| **APScheduler** | In-process | Низкая | Средняя | Ограничено | **Лучший выбор для бота** |
| **PTB JobQueue** | Встроенный | Низкая | Средняя | Ограничено | Если используется PTB |
| **Celery + Redis** | Distributed | Высокая | Высокая | Отличное | Для сложных систем |
| **asyncio.create_task** | In-process | Низкая | Низкая | Нет | Только для простых случаев |
| **systemd timers** | System | Средняя | Высокая | Нет | Для серверных задач |

### 3.2 Почему APScheduler — оптимальный выбор

- **Гибкость триггеров:** `CronTrigger`, `IntervalTrigger`, `DateTrigger`
- **Фоновое выполнение:** `BackgroundScheduler` не блокирует event loop
- **Интеграция с asyncio:** `AsyncIOScheduler` для async-кода
- **Job stores:** Хранение задач в памяти, PostgreSQL, Redis
- **Точное время:** Cron-выражения для точного времени уведомлений

### 3.3 Пример: утренние уведомления с APScheduler

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

async def send_morning_notification(user_id: int):
    """Отправка утреннего уведомления"""
    weather = await get_weather(user_id)
    news = await get_daily_news(user_id)
    message = f"☀ Доброе утро!\n\n{weather}\n\n📰 Новости:\n{news}"
    await bot.send_message(user_id, message)

# Добавление задачи для конкретного пользователя
def schedule_user_notification(user_id: int, time_str: str, timezone: str):
    hour, minute = map(int, time_str.split(":"))
    scheduler.add_job(
        send_morning_notification,
        trigger=CronTrigger(hour=hour, minute=minute, timezone=timezone),
        args=[user_id],
        id=f"morning_{user_id}",
        replace_existing=True,
    )

# Запуск планировщика
scheduler.start()
```

### 3.4 Когда выбрать Celery

- Необходимость **распределенных задач** (несколько worker-ов)
- Сложная **retry-логика** с отложенными попытками
- **Мониторинг задач** через Flower
- Интеграция с **RabbitMQ/Redis** как брокер
- Для бота с уведомлениями — избыточно, но полезно при масштабировании

---

## 4. Варианты деплоя и хостинга

### 4.1 VPS-хостинг (рекомендуется для 24/7 бота)

| Провайдер | Минимальный тариф | Локация | Плюсы | Минусы |
|-----------|-------------------|---------|-------|--------|
| **Hetzner** | ~4.51 EUR/мес | Германия, Финляндия | Дешевый, NVMe, надежный | Нет SLA, Европа |
| **DigitalOcean** | $5/мес | США, Европа, Сингапур | Простой, хорошие туториалы | Дороже Hetzner |
| **Timeweb** | ~200 руб/мес | Россия | **Серверы в РФ** (152-ФЗ) | Меньше ресурсов |
| **Beget** | ~200 руб/мес | Россия | **Серверы в РФ**, простой | Базовые возможности |
| **Selectel** | От 300 руб/мес | Россия | **Премиум РФ хостинг** | Дороже |
| **Vultr** | $2.50/мес | Мировые | Очень дешевый базовый | Минимум ресурсов |

### 4.2 Бесплатные/условно-бесплатные хостинги

| Платформа | Free Tier | Ограничения | Подходит для бота 24/7 |
|-----------|-----------|-------------|------------------------|
| **Render** | Есть | Spin down через 15 мин, cold start 30-60s | **Нет** (не подходит для уведомлений) |
| **Railway** | $5 trial credit | Нет free tier, pay-per-second | Да (начиная с $5/мес) |
| **Fly.io** | $5/мес credit | Сложная модель ценообразования | Да |
| **Heroku** | Eco $5/мес | Спит без трафика | Нет |
| **PythonAnywhere** | Есть | Ограниченные ресурсы | Частично |

> **Важно:** Для бота с утренними уведомлениями **бесплатные хостинги с spin-down не подходят** — бот должен работать 24/7.

### 4.3 Webhook vs Polling

| Критерий | Long Polling | Webhook |
|----------|-------------|---------|
| **Настройка** | Простая (start_polling) | Сложная (SSL + URL) |
| **Задержка** | ~1-3 секунды | Мгновенная |
| **Ресурсы** | Постоянное соединение | Только при событиях |
| **Публичный IP** | Не нужен | Нужен + SSL |
| **Масштабирование** | Только 1 инстанс | Несколько за load balancer |
| **Serverless** | Нет | Да |
| **Для 24/7 бота** | ✅ Да | ✅ Да (если есть SSL) |
| **Рекомендация** | **Для начала** | Для высокой нагрузки |

**Рекомендация для бота с уведомлениями:**
- **Polling** — для старта и разработки (проще, надежнее для перезапусков)
- **Webhook** — перейти при росте нагрузки (нужен домен + SSL)

### 4.4 Docker + systemd деплой

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

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

**systemd service (без Docker):**
```ini
# /etc/systemd/system/telegram-bot.service
[Unit]
Description=Telegram Morning Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/telegram-bot
ExecStart=/opt/telegram-bot/venv/bin/python -m bot.main
Restart=always
RestartSec=5
Environment=PYTHONPATH=/opt/telegram-bot

[Install]
WantedBy=multi-user.target
```

---

## 5. Рекомендуемая архитектура

### 5.1 Архитектура: Монолит (для старта)

```
┌─────────────────────────────────────────────────────────────┐
│                       Telegram API                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    aiogram 3.x Bot                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Handlers   │  │   FSM        │  │   Middleware     │   │
│  │  (команды)   │  │  (состояния) │  │ (rate limit,     │   │
│  │              │  │              │  │  logging)        │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Services Layer                           │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │    │
│  │  │Weather  │ │ News    │ │ AI      │ │Scheduler │  │    │
│  │  │Service  │ │ Service │ │ Service │ │Service   │  │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └──────────┘  │    │
│  └──────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Data Layer                               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │SQLAlchemy│  │  Redis   │  │APScheduler│          │    │
│  │  │  (ORM)   │  │ (Cache)  │  │(Tasks)    │          │    │
│  │  └────┬─────┘  └──────────┘  └──────────┘           │    │
│  │       │                                              │    │
│  │  ┌────▼─────┐                                        │    │
│  │  │PostgreSQL│                                        │    │
│  │  │ (Users,  │                                        │    │
│  │  │ Settings)│                                        │    │
│  │  └──────────┘                                        │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Переход к микросервисам (при масштабировании)

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway / LB                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌────────▼───────┐  ┌────────▼───────┐
│   Bot Core   │  │ Notification   │  │     AI         │
│  (Telegram)  │  │   Service      │  │   Service      │
│              │  │ (Scheduler)    │  │ (LLM API)      │
└──────┬───────┘  └───────┬────────┘  └───────┬────────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
              ┌───────────▼───────────┐
              │    Message Queue      │
              │    (Redis/RabbitMQ)   │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   Shared Database     │
              │     (PostgreSQL)      │
              └───────────────────────┘
```

### 5.3 Обработка ошибок и retry-логика

```python
import asyncio
from functools import wraps
from loguru import logger

def retry(max_retries=3, delay=1, backoff=2):
    """Декоратор retry с экспоненциальным backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Failed after {max_retries} retries: {e}")
                        raise
                    logger.warning(f"Attempt {retries} failed: {e}. Retrying in {current_delay}s...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

@retry(max_retries=3, delay=1, backoff=2)
async def send_morning_notification(user_id: int):
    """Отправка уведомления с retry-логикой"""
    # ... логика отправки
```

### 5.4 Логирование

Рекомендуется **loguru** — современная альтернатива стандартному logging:

```python
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/bot.log", rotation="10 MB", retention="7 days", level="INFO")
logger.add("logs/errors.log", rotation="10 MB", retention="30 days", level="ERROR")
```

### 5.5 Мониторинг

| Инструмент | Назначение | Цена |
|------------|-----------|------|
| **UptimeRobot** | Проверка доступности webhook/health endpoint | Бесплатно (5 мин интервал) |
| **Healthchecks.io** | Проверка heartbeat от бота (cron jobs) | Бесплатно |
| **Grafana + Prometheus** | Полноценный мониторинг метрик | Бесплатно (self-hosted) |
| **Sentry** | Отслеживание ошибок в коде | Бесплатно (до 5000 событий) |

**Health check endpoint (для webhook-режима):**
```python
from aiohttp import web

async def health_check(request):
    return web.Response(text="OK", status=200)

app = web.Application()
app.router.add_get("/health", health_check)
```

### 5.6 Обновления без перезапуска

- **Docker:** `docker-compose pull && docker-compose up -d` (zero-downtime с restart: always)
- **systemd:** `systemctl reload telegram-bot` (требует обработки SIGHUP в коде)
- **Hot-reload:** Для разработки — `watchdog` или `entr`

---

## 6. Безопасность

### 6.1 Хранение API-ключей

```python
# .env (добавить в .gitignore!)
BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_key_here
WEATHER_API_KEY=your_weather_key_here
DATABASE_URL=postgresql://user:pass@localhost/botdb
REDIS_URL=redis://localhost:6379/0

# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    weather_api_key: str
    database_url: str
    redis_url: str
    admin_ids: list[int] = []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 6.2 Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 5, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: int) -> bool:
        now = datetime.now()
        user_requests = self.requests[user_id]
        user_requests[:] = [r for r in user_requests if now - r < timedelta(seconds=self.window)]
        
        if len(user_requests) >= self.max_requests:
            return False
        
        user_requests.append(now)
        return True

rate_limiter = RateLimiter(max_requests=10, window=60)  # 10 запросов в минуту
```

### 6.3 Защита от спама

- Rate limiting по user_id (10-20 сообщений/минуту)
- Проверка входных данных (длина сообщения, допустимые символы)
- Каптча для новых пользователей ( через @BotFather или reCAPTCHA)
- Бан по подозрительной активности
- Фильтрация нежелательного контента через AI

### 6.4 Обработка персональных данных (152-ФЗ)

> **Критически важно:** С 1 июля 2025 года вступили в силу новые правила локализации персональных данных (23-ФЗ).

**Требования:**
1. **Базы данных с ПД россиян должны находиться на территории РФ**
   - Хостинг должен быть в России (Timeweb, Beget, Selectel)
   - Или использовать российские облака (Yandex Cloud, VK Cloud)
2. **Штрафы:** до 6 млн руб за первое нарушение, до 18 млн руб за повторное (420-ФЗ)
3. **Обязанности оператора:**
   - Уведомление пользователей о сборе данных
   - Получение согласия на обработку
   - Возможность удаления данных по запросу
   - Размещение политики конфиденциальности
4. **Что собирать минимально:**
   - Только `telegram_id` (не считается ПД без привязки к имени)
   - username — только при согласии
   - Не хранить сообщения пользователей

**Рекомендация:**
```python
# Минимизация сбора данных
class UserMinimal(Base):
    __tablename__ = "users"
    
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    notification_time: Mapped[str] = mapped_column(String(5), default="08:00")
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    # НЕ храним: username, first_name, last_name (это ПД!)
```

---

## 7. Пример структуры проекта

```
telegram-morning-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Точка входа, запуск бота
│   ├── config.py            # Конфигурация (Pydantic Settings)
│   ├── constants.py         # Константы
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── commands.py      # /start, /help, /settings
│   │   ├── messages.py      # Обработка текстовых сообщений
│   │   ├── callbacks.py     # Inline keyboard callbacks
│   │   └── admin.py         # Админ-команды
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather.py       # API погоды
│   │   ├── news.py          # API новостей
│   │   ├── ai_service.py    # AI-ответы (OpenAI/LLM)
│   │   └── scheduler.py     # APScheduler задачи
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # SQLAlchemy модели
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── logging.py       # Логирование запросов
│   │   └── rate_limit.py    # Rate limiting
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py        # Inline keyboards
│   ├── states/
│   │   ├── __init__.py
│   │   └── settings.py      # FSM состояния
│   └── utils/
│       ├── __init__.py
│       ├── retry.py         # Retry-логика
│       └── validators.py    # Валидация данных
├── migrations/              # Alembic миграции
├── logs/                    # Логи (в .gitignore)
├── tests/
│   ├── __init__.py
│   └── test_handlers.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .env                     # В .gitignore!
├── .gitignore
└── README.md
```

### 7.1 requirements.txt

```
# Core
aiogram==3.28.0
aiohttp==3.11.0

# Database
SQLAlchemy==2.0.36
aiosqlite==0.20.0
asyncpg==0.30.0
alembic==1.14.0
redis==5.2.0

# Scheduler
APScheduler==3.11.0

# Configuration & Validation
pydantic==2.10.0
pydantic-settings==2.7.0
python-dotenv==1.0.1

# Logging
loguru==0.7.3

# HTTP Client
httpx==0.28.0

# AI Integration
openai==1.60.0

# Monitoring
sentry-sdk==2.19.0
```

### 7.2 main.py — точка входа

```python
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import settings
from bot.handlers import commands, messages, callbacks
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.rate_limit import RateLimitMiddleware
from bot.services.scheduler import setup_scheduler
from bot.database import init_db

async def main():
    # Инициализация
    await init_db()
    
    # Redis storage для FSM
    storage = RedisStorage.from_url(settings.redis_url)
    
    # Bot + Dispatcher
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    
    # Middleware
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    
    # Routers
    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(messages.router)
    
    # Scheduler для уведомлений
    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot)
    scheduler.start()
    
    # Запуск
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. Итоговые рекомендации

### 8.1 Оптимальный стек для бота с утренними уведомлениями

| Компонент | Рекомендация | Альтернатива |
|-----------|-------------|--------------|
| **Фреймворк** | aiogram 3.x | python-telegram-bot 22.x |
| **База данных** | PostgreSQL | SQLite (для старта) |
| **Кэш/FSM** | Redis | MemoryStorage (только dev) |
| **ORM** | SQLAlchemy 2.0 | Tortoise ORM |
| **Планировщик** | APScheduler (AsyncIOScheduler) | PTB JobQueue |
| **Хостинг** | VPS Hetzner/DigitalOcean | Timeweb (для РФ — 152-ФЗ) |
| **Контейнеризация** | Docker + docker-compose | systemd service |
| **Мониторинг** | UptimeRobot + Sentry | Grafana + Prometheus |
| **Логирование** | loguru | structlog |
| **AI** | OpenAI API | Claude API, локальные LLM |
| **CI/CD** | GitHub Actions | GitLab CI |

### 8.2 Порядок разработки

1. **MVP (неделя 1):**
   - aiogram 3.x + SQLite + MemoryStorage
   - Базовые команды (/start, /help)
   - Ручной запрос погоды
   
2. **Core (неделя 2):**
   - PostgreSQL + Redis + SQLAlchemy
   - APScheduler + утренние уведомления
   - AI-интеграция
   
3. **Production (неделя 3):**
   - Docker + деплой на VPS
   - Мониторинг + логирование
   - Rate limiting + безопасность
   - 152-ФЗ compliance (если целевая аудитория в РФ)

### 8.3 Ожидаемые затраты

| Компонент | Стоимость/мес |
|-----------|--------------|
| VPS (Hetzner CX11) | ~4.51 EUR |
| Или VPS (DigitalOcean) | $5 |
| Или VPS (Timeweb) | ~200-300 руб |
| OpenAI API | $1-10 (зависит от нагрузки) |
| Weather API | Бесплатно (OpenWeatherMap) |
| UptimeRobot | Бесплатно |
| Sentry | Бесплатно |
| **Итого минимум** | **~$5-7/мес** |

### 8.4 Полезные ссылки

- **aiogram 3 docs:** https://docs.aiogram.dev/
- **python-telegram-bot docs:** https://docs.python-telegram-bot.org/
- **APScheduler docs:** https://apscheduler.readthedocs.io/
- **SQLAlchemy 2 docs:** https://docs.sqlalchemy.org/
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **152-ФЗ (консультант):** https://www.consultant.ru/document/cons_doc_LAW_61801/
- **Redis docs:** https://redis.io/docs/
- **Docker docs:** https://docs.docker.com/

---

*Исследование подготовлено на основе актуальных данных июля 2025 года. Технологии регулярно обновляются — рекомендуется проверять актуальность версий перед деплоем.*
