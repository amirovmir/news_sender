# news_sender — Design Spec
**Дата:** 2026-06-29

## Контекст

Telegram-бот, который каждое утро в 7:00 UTC+3 присылает пользователям мотивационное сообщение, прогноз погоды и краткую сводку мировых и российских новостей. Дополнительно бот умеет отвечать на произвольные вопросы через AI. Рассчитан на несколько пользователей, каждый из которых выбирает свой город. Деплой на VPS через Docker Compose.

---

## Архитектура

**Стек:**
- Python 3.11 + aiogram 3.x (polling)
- PostgreSQL 16 — хранение пользователей и истории диалогов
- Redis 7 — FSM storage + кэш AI-контекста
- APScheduler 3.x (AsyncIOScheduler + CronTrigger) — утренние рассылки
- Docker Compose — единый деплой (bot + db + redis)

**Внешние API (все бесплатные):**
| Назначение | API | Ключ |
|---|---|---|
| Погода | Open-Meteo | Не нужен |
| Геокодирование города | Open-Meteo geocoding | Не нужен |
| Новости РФ | РИА, ТАСС, Лента.ру, РБК (RSS) | Не нужен |
| Мировые новости | Google News RSS (`hl=ru`) | Не нужен |
| AI primary | Groq (llama-3.3-70b-versatile) | `GROQ_API_KEY` |
| AI fallback | Google Gemini 2.5 Flash | `GEMINI_API_KEY` |

---

## Структура проекта

```
news_sender/
├── bot/
│   ├── main.py              # точка входа: Bot, Dispatcher, scheduler, polling
│   ├── config.py            # Pydantic Settings (читает .env)
│   ├── database.py          # SQLAlchemy async engine, get_session, init_db
│   ├── handlers/
│   │   ├── commands.py      # /start, /help, /weather, /news, /settings
│   │   ├── messages.py      # F.text → ai_service.ask()
│   │   └── callbacks.py     # кнопки меню и настроек
│   ├── services/
│   │   ├── weather.py       # get_weather_text(lat, lon, city_name) → str
│   │   ├── news.py          # get_news_summary() → str (RSS + AI суммаризация)
│   │   ├── ai_service.py    # ask(question, history) → str; Groq → Gemini fallback
│   │   └── scheduler.py     # setup_scheduler(), send_morning_digest()
│   ├── models/
│   │   └── user.py          # User, ChatHistory (SQLAlchemy 2.0 Mapped)
│   └── keyboards/
│       └── inline.py        # main_menu(), settings_menu()
├── deployments/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── requirements.txt
└── .gitignore
```

---

## База данных

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    city_name VARCHAR(100) DEFAULT 'Москва',
    city_lat FLOAT DEFAULT 55.7558,
    city_lon FLOAT DEFAULT 37.6173,
    notification_time VARCHAR(5) DEFAULT '07:00',  -- HH:MM UTC+3
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,   -- 'user' | 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Миграции через Alembic.

---

## Утреннее сообщение

Структура сообщения в 7:00 UTC+3:

```
🌅 Доброе утро!

💪 <мотивационная фраза — генерируется Groq>

━━━━━━━━━━━━━━━

🌤 Погода: <город>
<температура, ощущается, влажность, ветер>
Прогноз на день: макс/мин, осадки

━━━━━━━━━━━━━━━

📰 Главные новости
<AI-суммаризация топ-5 тем из RSS за последние 24 часа>

━━━━━━━━━━━━━━━
💬 Задайте мне любой вопрос!
```

**Логика планировщика:**
- При старте бота `setup_scheduler()` загружает всех активных пользователей из БД
- Для каждого создаётся APScheduler job с `CronTrigger(hour=7, minute=0, timezone='Europe/Moscow')`
- При изменении настроек пользователя job пересоздаётся (`replace_existing=True`)
- Время уведомления фиксировано 7:00 UTC+3, но пользователь может его менять через /settings

---

## AI-чат

- Любой текст, не являющийся командой → `ai_service.ask(text, history)`
- История: последние 10 сообщений пользователя из `chat_history`, передаются в messages[]
- Primary: Groq `llama-3.3-70b-versatile`, max_tokens=1500
- Fallback: Gemini `gemini-2.5-flash` при ошибке Groq (rate limit, timeout)
- Системный промпт: "Ты дружелюбный ассистент в Telegram. Отвечай на русском языке. Используй HTML-форматирование."

---

## Настройки пользователя (/settings)

FSM-диалог:
1. Пользователь нажимает «Изменить город»
2. Бот просит написать название города
3. Open-Meteo geocoding API переводит название → lat/lon
4. Город сохраняется в БД, job планировщика пересоздаётся

Доступные команды:
| Команда | Описание |
|---|---|
| /start | Приветствие + регистрация пользователя |
| /weather | Текущая погода для города пользователя |
| /news | Ручной запрос сводки новостей |
| /settings | Изменить город / время уведомления / вкл-выкл |
| /help | Список команд |

---

## Деплой

```yaml
# docker-compose.yml (сокращённо)
services:
  bot:
    build: .
    restart: always
    env_file: deployments/.env
    depends_on: [db, redis]
  db:
    image: postgres:16-alpine
    volumes: [postgres_data:/var/lib/postgresql/data]
  redis:
    image: redis:7-alpine
```

VPS: любой с 1GB RAM (Hetzner CX11 ~5€/мес). Деплой: `git pull && docker compose up -d --build`.

---

## Обработка ошибок

- Все обращения к внешним API обёрнуты в try/except с логированием через `loguru`
- RSS: если источник недоступен — пропускается, суммаризируются доступные
- AI fallback: Groq → Gemini → сообщение "Сервис временно недоступен"
- Погода: если Open-Meteo недоступен — пропускается блок погоды в утреннем сообщении с пометкой
- Scheduler: ошибка отправки одному пользователю не прерывает рассылку остальным

---

## Нет в scope

- Голосовые сообщения
- Inline-режим
- Аналитика / Grafana
- Мультиязычность интерфейса
- Платные AI-модели
