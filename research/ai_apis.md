# AI API для Telegram-бота — Глубокое исследование 2025-2026

> **Дата исследования:** Июль 2026
> **Цель:** Найти все доступные бесплатные и дешёвые API для интеграции AI-ответов в Telegram-бот с поддержкой русского языка.
> **Методология:** Анализ официальной документации, pricing-страниц и бенчмарков 15+ провайдеров.

---

## Сравнительная таблица (быстрый обзор)

| # | API | Бесплатно | Лимиты | Модели | Русский язык | Скорость | Рейтинг |
|---|-----|-----------|--------|--------|-------------|----------|---------|
| 1 | **Kimi API (Moonshot AI)** | Нет (min $1) | Зависит от баланса | K2.5, K2.6 | ⭐⭐⭐⭐⭐ Отличный | Средняя | ★★★★☆ |
| 2 | **OpenRouter** | ✅ Да | 20 RPM, 50-200 RPD | 200+ моделей | ⭐⭐⭐⭐ Зависит от модели | Средняя | ★★★★★ |
| 3 | **OpenAI API** | ⚠️ Нестабильно | ~$5 trial | GPT-4o, GPT-5.4 mini | ⭐⭐⭐⭐⭐ Отличный | Быстрая | ★★★☆☆ |
| 4 | **Google Gemini API** | ✅ Да | ~1,500 req/day (Flash) | Gemini 2.5 Flash/Flash-Lite | ⭐⭐⭐⭐ Хороший | Быстрая | ★★★★☆ |
| 5 | **Anthropic Claude API** | ⚠️ ~$5 trial | Нет постоянного free tier | Sonnet 4.6, Haiku 4.5 | ⭐⭐⭐⭐⭐ Отличный | Средняя | ★★★☆☆ |
| 6 | **Groq API** | ✅ Да | 30 RPM, 1,000-14,400 RPD | Llama, Qwen, Whisper | ⭐⭐⭐⭐ Хороший | ⭐⭐⭐⭐⭐ Очень быстрая | ★★★★★ |
| 7 | **Cohere API** | ✅ Trial key | Rate limited | Command R/R+ | ⭐⭐⭐ Средний | Средняя | ★★★☆☆ |
| 8 | **Mistral AI API** | ✅ Да | ~1B tokens/month (open-weight) | Mistral Large/Small/Nemo | ⭐⭐⭐⭐ Хороший | Быстрая | ★★★★☆ |
| 9 | **DeepSeek API** | ✅ 5M tokens | 30 дней, потом pay-as-you-go | V4 Flash, V4 Pro, R1 | ⭐⭐⭐⭐⭐ Отличный | Быстрая | ★★★★★ |
| 10 | **Ollama (локально)** | ✅ Полностью | Безлимитно | Любые GGUF модели | ⭐⭐⭐⭐ Зависит от модели | Зависит от GPU | ★★★★☆ |
| 11 | **LM Studio** | ✅ Полностью | Безлимитно | Любые GGUF модели | ⭐⭐⭐⭐ Зависит от модели | Зависит от GPU | ★★★★☆ |
| 12 | **llama.cpp** | ✅ Полностью | Безлимитно | GGUF формат | ⭐⭐⭐⭐ Зависит от модели | Зависит от GPU | ★★★★☆ |
| 13 | **HuggingFace Inference** | ✅ Да | Несколько сотен req/hr | Тысячи open-source | ⭐⭐⭐ Зависит от модели | Медленная (cold start) | ★★★☆☆ |
| 14 | **Together AI** | ❌ Нет | Минимум $5 | 100+ open-source | ⭐⭐⭐⭐ Хороший | Быстрая | ★★☆☆☆ |
| 15 | **Perplexity API** | ❌ Нет | Pro: $5 API credits/мес | Sonar, Sonar Pro | ⭐⭐⭐⭐ Хороший | Быстрая | ★★☆☆☆ |
| 16 | **Cerebras** | ✅ Да | 1M tokens/day | GPT-OSS-120B, Qwen3 | ⭐⭐⭐⭐ Хороший | ⭐⭐⭐⭐⭐ Очень быстрая | ★★★★★ |
| 17 | **GitHub Models** | ✅ Да | 10 RPM, 50-150 RPD | GPT-5, Llama-4, Mistral | ⭐⭐⭐⭐⭐ Отличный | Средняя | ★★★★☆ |
| 18 | **Cloudflare Workers AI** | ✅ Да | 10K Neurons/day | Llama, Mistral, DeepSeek | ⭐⭐⭐⭐ Хороший | ⭐⭐⭐⭐⭐ Очень быстрая | ★★★★☆ |
| 19 | **SambaNova** | ✅ Да (+$5 credit) | 20 RPM, 200K tokens/day | Llama, DeepSeek | ⭐⭐⭐⭐ Хороший | Быстрая | ★★★☆☆ |

---

## Облачные API

---

### 1. Kimi API (Moonshot AI)

**🔗 Ссылки:**
- Документация: https://platform.moonshot.ai/docs
- API endpoint: `https://api.moonshot.ai/v1`
- Сайт: https://kimi.com

**💰 Стоимость / бесплатные лимиты:**
- **Нет постоянного бесплатного тарифа.** Требуется минимальное пополнение на **$1** для активации API.
- При пополнении на $5+ — бонусный ваучер $5.
- Цены (прямой API):
  - Kimi K2.5: $0.60/M input tokens, $2.50-3.00/M output tokens
  - Kimi K2.6: $0.95/M input (cache miss), $0.16/M (cache hit), $4.00/M output
- Через OpenRouter: $0.45/M input, $2.20/M output (дешевле!)
- Через Together AI: $0.50/M input, $2.80/M output

**🤖 Доступные модели:**
- `kimi-k2.5` — основная модель, 256K контекст, мультимодальная
- `kimi-k2.6` — open-source модель, 262K контекст, coding + agents
- `kimi-k2-turbo` — ускоренная версия
- `kimi-k2-thinking` — модель с chain-of-thought reasoning

**🗣️ Русский язык:** ⭐⭐⭐⭐⭐ — Kimi отлично понимает и генерирует русский текст. Moonshot AI — китайская компания, и модели хорошо обучены на мультилингвальных данных, включая русский.

**⚡ Скорость:** Средняя. Не такая быстрая, как Groq или Cerebras, но приемлемая для чат-бота.

**✅ Плюсы:**
- OpenAI-совместимый API (простая миграция)
- Огромный контекст (256K токенов)
- Отличное качество на русском
- Очень конкурентные цены
- Автоматическое кэширование контекста (экономия до 75%)
- Модифицированная MIT лицензия (open-source)

**❌ Минусы:**
- Нет бесплатного tier (нужно $1 для активации)
- Китайская платформа — интерфейс может быть на китайском
- Меньшая экосистема инструментов по сравнению с OpenAI

**🔑 Как получить доступ:**
1. Зарегистрироваться на platform.moonshot.ai
2. Пополнить баланс минимум на $1
3. Создать API ключ в разделе API Keys

**📌 Пример кода Python:**
```python
import openai

client = openai.OpenAI(
    api_key="sk-YOUR_MOONSHOT_API_KEY",
    base_url="https://api.moonshot.ai/v1"
)

response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "system", "content": "Ты — полезный ассистент. Отвечай на русском языке."},
        {"role": "user", "content": "Объясни, как работает API Telegram ботов"}
    ],
    temperature=0.7,
    max_tokens=1000
)
print(response.choices[0].message.content)
```

---

### 2. OpenRouter

**🔗 Ссылки:**
- Сайт: https://openrouter.ai
- Документация: https://openrouter.ai/docs
- API endpoint: `https://openrouter.ai/api/v1`

**💰 Стоимость / бесплатные лимиты:**
- **27+ бесплатных моделей** (с суффиксом `:free`)
- 20 RPM (запросов в минуту)
- 50 RPD (запросов в день) для новых/неверифицированных аккаунтов
- **1,000 RPD** после единоразовой покупки кредитов на $10
- Нет ежемесячных платежей — кредиты не истекают

**🤖 Доступные бесплатные модели (лучшие для Telegram-бота):**
- `deepseek/deepseek-r1:free` — лучший бесплатный reasoning
- `meta-llama/llama-3.3-70b-instruct:free` — сильная общая модель
- `meta-llama/llama-4-scout:free` — 10M контекст + мультимодальная
- `qwen/qwen3-235b-a22b:free` — мультиязычная (отличный русский!)
- `google/gemma-3-12b-it:free` — быстрая, лёгкая
- `mistralai/mistral-7b-instruct:free` — лёгкий fallback

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Зависит от модели. Qwen3, DeepSeek R1 и Llama 3.3 отлично работают с русским.

**⚡ Скорость:** Средняя. Зависит от конкретной модели и загрузки. Бесплатные модели могут быть медленнее в часы пик.

**✅ Плюсы:**
- Один API ключ для 200+ моделей от 50+ провайдеров
- Не требует кредитной карты для бесплатных моделей
- Простое переключение между моделями (один параметр `model`)
- OpenAI-совместимый формат
- Можно комбинировать несколько бесплатных моделей для обхода лимитов

**❌ Минусы:**
- Бесплатные модели имеют строгие лимиты
- В часы пик возможны rate limit errors (429)
- Бесплатные провайдеры могут логировать промпты
- Качество ответов варьируется в зависимости от модели

**🔑 Как получить доступ:**
1. Зарегистрироваться на openrouter.ai (email или Google)
2. Создать API ключ в Dashboard
3. Использовать модели с суффиксом `:free`

**📌 Пример кода Python:**
```python
import requests

API_KEY = "sk-or-v1-YOUR_OPENROUTER_KEY"

def ask_openrouter(prompt, model="deepseek/deepseek-r1:free"):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-bot.com",
            "X-Title": "Telegram Bot"
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "Ты — полезный ассистент. Отвечай на русском языке."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    )
    return response.json()["choices"][0]["message"]["content"]

# Использование
answer = ask_openrouter("Расскажи о достопримечательностях Москвы")
print(answer)
```

**💡 Стратегия обхода лимитов:** Используйте несколько моделей по очереди:
```python
FREE_MODELS = [
    "deepseek/deepseek-r1:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen3-235b-a22b:free",
    "google/gemma-3-12b-it:free"
]
```

---

### 3. OpenAI API

**🔗 Ссылки:**
- Документация: https://platform.openai.com/docs
- API endpoint: `https://api.openai.com/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Нет стабильного бесплатного tier.** Ранее давали ~$5 trial credits новым аккаунтам — теперь это непоследовательно.
- Есть "data sharing" программа — бесплатные токены за согласие на использование данных.
- Программа OpenAI for Startups — до $50K credits.
- GPT-4o mini: $0.15/M input, $0.60/M output (самые дешёвые у OpenAI)
- GPT-5.4 mini: $0.75/M input, $4.50/M output

**🤖 Доступные модели:**
- GPT-4o mini — быстрый, дешёвый, хорошее качество
- GPT-4o — флагманская модель
- GPT-5.4 mini — новое поколение

**🗣️ Русский язык:** ⭐⭐⭐⭐⭐ — Лучший среди всех API. GPT-4o и GPT-5 отлично понимают нюансы русского языка.

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Лучшее качество ответов
- Отличная поддержка русского
- Самая зрелая экосистема
- GPT-4o mini — доступная цена для небольшого бота

**❌ Минусы:**
- Нет гарантированного бесплатного tier
- Дороже конкурентов
- Нужна кредитная карта

**🔑 Как получить доступ:**
1. Зарегистрироваться на platform.openai.com
2. Привязать кредитную карту
3. Создать API ключ

**📌 Пример кода Python:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-YOUR_OPENAI_KEY")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Ты — полезный Telegram-бот. Отвечай на русском."},
        {"role": "user", "content": "Привет! Как дела?"}
    ],
    max_tokens=500,
    temperature=0.7
)
print(response.choices[0].message.content)
```

---

### 4. Google Gemini API

**🔗 Ссылки:**
- Документация: https://ai.google.dev/gemini-api/docs
- API endpoint: `https://generativelanguage.googleapis.com`

**💰 Стоимость / бесплатные лимиты:**
- **Бесплатный tier:** ~1,500 requests/day для Gemini 2.5 Flash
- 10 RPM (запросов в минуту)
- В конце 2025 Google сильно сократил бесплатные лимиты (было ~250 RPD, стало ~20 RPD для некоторых моделей)
- Gemini 2.5 Flash-Lite: до 1,500 RPD (самый щедрый лимит)
- Gemini 2.5 Pro: убран из бесплатного tier (только paid)
- Не требуется кредитная карта

**🤖 Доступные модели (бесплатно):**
- `gemini-2.5-flash` — основная модель, быстрая
- `gemini-2.5-flash-lite` — самая дешевая, высокие лимиты
- `gemini-2.0-flash` — предыдущее поколение

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Хороший. Gemini хорошо понимает русский, но иногда уступает GPT-4o в нюансах.

**⚡ Скорость:** Быстрая, особенно Flash-модели.

**✅ Плюсы:**
- Щедрый бесплатный tier (1,500+ запросов/день)
- Не требует кредитной карты
- Отличная мультимодальность (текст, изображения, видео, аудио)
- Большой контекст (до 1M токенов)
- Надёжность и стабильность Google

**❌ Минусы:**
- Лимиты сокращаются (тренд 2025-2026)
- Нет бесплатного доступа к Pro-моделям
- Данные используются для улучшения продуктов Google (можно отключить)

**🔑 Как получить доступ:**
1. Перейти на ai.google.dev
2. Получить API ключ (требуется Google аккаунт)
3. Начать использовать сразу

**📌 Пример кода Python:**
```python
import google.generativeai as genai

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

response = model.generate_content(
    "Расскажи интересные факты о Санкт-Петербурге",
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1000
    )
)
print(response.text)
```

---

### 5. Anthropic Claude API

**🔗 Ссылки:**
- Документация: https://docs.anthropic.com
- API endpoint: `https://api.anthropic.com/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Нет постоянного бесплатного tier.**
- Новые аккаунты получают ~$5 trial credits (после верификации телефона)
- Программа для open-source разработчиков: 6 месяцев Claude Max 20x бесплатно
- Haiku 4.5: $1/M input, $5/M output (самая дешевая модель Claude)
- Sonnet 4.6: $3/M input, $15/M output
- Batch API: скидка 50%

**🤖 Доступные модели:**
- Claude Haiku 4.5 — быстрая, дешевая
- Claude Sonnet 4.6 — лучший баланс качества/цены
- Claude Opus 4.7/4.8 — флагман, дорогой

**🗣️ Русский язык:** ⭐⭐⭐⭐⭐ — Claude отлично работает с русским языком, особенно на задачах анализа и написания текста.

**⚡ Скорость:** Средняя

**✅ Плюсы:**
- Лучшее качество reasoning и анализа
- Отличный русский язык
- Огромный контекст (до 1M токенов)
- Prompt caching (90% скидка на повторные запросы)

**❌ Минусы:**
- Нет бесплатного tier
- Дорогой ($5 trial хватит на ~150-300 коротких запросов)
- Нужна кредитная карта

**📌 Пример кода Python:**
```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-api03-YOUR_KEY")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Напиши краткое руководство по созданию Telegram бота на Python"}
    ]
)
print(response.content[0].text)
```

---

### 6. Groq API

**🔗 Ссылки:**
- Сайт: https://groq.com
- Документация: https://console.groq.com/docs
- API endpoint: `https://api.groq.com/openai/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Полностью бесплатный tier** — не требуется кредитная карта
- 30 RPM (запросов в минуту)
- 6,000 TPM (токенов в минуту)
- 1,000-14,400 RPD (зависит от модели)
- Лимиты применяются на уровне организации (не per-key)
- Developer tier: +25% скидка, 10x лимиты (требуется карта, минимум $0)

**🤖 Доступные модели (бесплатно):**
- `llama-3.3-70b-versatile` — 1,000 RPD
- `llama-3.1-8b-instant` — 14,400 RPD
- `llama-4-scout-17b-16e-instruct` — 1,000 RPD, 10M контекст!
- `qwen3-32b` — 1,000 RPD
- `meta-llama/llama-4-maverick` — 1,000 RPD
- `whisper-large-v3` — 2,000 audio запросов/день

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Llama 3.3 и Qwen3 хорошо работают с русским. Qwen3 особенно силён в китайском и русском.

**⚡ Скорость:** ⭐⭐⭐⭐⭐ — **Самый быстрый API на рынке!** LPUs (Language Processing Units) дают 1,500-3,000 токенов/секунду и sub-100ms время до первого токена.

**✅ Плюсы:**
- Не требует кредитной карты
- Самая высокая скорость inference на рынке
- Llama 4 Scout с 10M контекстом бесплатно
- OpenAI-совместимый API
- Whisper для распознавания речи

**❌ Минусы:**
- Только open-source модели (нет GPT/Claude)
- Лимиты могут быть недостаточны для большого бота
- TPM лимит (6,000) — длинные промпты быстро исчерпают лимит

**🔑 Как получить доступ:**
1. Зарегистрироваться на console.groq.com (~30 секунд)
2. Создать API ключ
3. Начать использовать сразу

**📌 Пример кода Python:**
```python
from groq import Groq

client = Groq(api_key="gsk_YOUR_GROQ_KEY")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Ты — дружелюбный Telegram-бот. Отвечай на русском."},
        {"role": "user", "content": "Что интересного можно посмотреть в Казани?"}
    ],
    temperature=0.7,
    max_tokens=800
)
print(response.choices[0].message.content)
```

---

### 7. Cohere API

**🔗 Ссылки:**
- Сайт: https://cohere.com
- API endpoint: `https://api.cohere.ai/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Trial API ключ бесплатно** — rate limited, не для production
- Command R: $0.50/M input, $1.50/M output
- Command R+: $2.50/M input, $10/M output
- Rerank модели: от $0.001-0.0025/search

**🤖 Доступные модели:**
- Command R / R+ — основные LLM
- Rerank модели — для поиска и RAG
- Embed модели — для эмбеддингов

**🗣️ Русский язык:** ⭐⭐⭐ — Средний. Cohere ориентирован на английский, но поддерживает мультиязычность через Command R.

**⚡ Скорость:** Средняя

**✅ Плюсы:**
- Бесплатный trial ключ
- Отличные RAG-возможности (rerank + embeddings)
- Структурированные выходы (JSON mode)

**❌ Минусы:**
- Ограниченный бесплатный tier
- Русский язык не на уровне GPT/Claude
- Trial ключи не для коммерческого использования

**📌 Пример кода Python:**
```python
import cohere

co = cohere.Client("YOUR_COHERE_API_KEY")

response = co.chat(
    model="command-r",
    message="Расскажи о лучших практиках разработки Telegram ботов",
    preamble="Ты — эксперт по разработке чат-ботов. Отвечай на русском языке."
)
print(response.text)
```

---

### 8. Mistral AI API

**🔗 Ссылки:**
- Сайт: https://mistral.ai
- Платформа: https://console.mistral.ai
- API endpoint: `https://api.mistral.ai/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Free Experiment tier** — доступ ко всем моделям, rate limited
- ~1 миллиард токенов/месяц для open-weight моделей
- ~1 req/sec, ~30 req/min
- Не требуется кредитная карта (только SMS-верификация)
- Mistral Nemo: $0.02/M input — самая дешевая модель среди tier-1 провайдеров!
- Mistral Small 4: $0.15/M input, $0.60/M output
- Mistral Large 3: $0.50/M input, $1.50/M output

**🤖 Доступные модели:**
- `mistral-large-3` — флагман, 262K контекст
- `mistral-small-4` — быстрая, 128K контекст
- `codestral` — для кода, 32K контекст
- `mistral-nemo` — самая дешевая, мультиязычная
- Open-weight модели: Mixtral 8x7B, Mistral 7B (бесплатно для self-hosting)

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Хороший. Mistral Nemo и Large 3 хорошо работают с русским. Однако Mistral традиционно сильнее во французском и испанском.

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Очень щедрый бесплатный tier (~1B tokens/мес)
- Самые низкие цены среди tier-1 провайдеров
- EU-инфраструктура (GDPR compliance)
- Open-weight модели для self-hosting
- Prompt caching (90% скидка)

**❌ Минусы:**
- Rate limits на бесплатном tier
- Русский язык немного уступает GPT/Claude
- Free tier — только для open-weight моделей

**📌 Пример кода Python:**
```python
from mistralai import Mistral

client = Mistral(api_key="YOUR_MISTRAL_KEY")

response = client.chat.complete(
    model="mistral-large-3",
    messages=[
        {"role": "system", "content": "Ты — полезный ассистент на русском языке."},
        {"role": "user", "content": "Как настроить вебхук для Telegram бота?"}
    ]
)
print(response.choices[0].message.content)
```

---

### 9. DeepSeek API

**🔗 Ссылки:**
- Сайт: https://deepseek.ai
- Платформа: https://platform.deepseek.com
- API endpoint: `https://api.deepseek.com/v1`

**💰 Стоимость / бесплатные лимиты:**
- **5 миллионов бесплатных токенов** при регистрации (~$8 стоимости)
- Действуют 30 дней, не требуется кредитная карта
- После исчерпания — очень дешёвый pay-as-you-go:
  - V4 Flash: $0.14/M input, $0.28/M output (cache miss)
  - V4 Flash cache hit: $0.0028/M (98% экономия!)
  - V4 Pro: $1.74/M input, $3.48/M output
- Скидки в off-peak часы: до 75%

**🤖 Доступные модели:**
- `deepseek-v4-flash` — быстрая, дешевая, с reasoning
- `deepseek-v4-pro` — флагманская reasoning модель
- `deepseek-r1` — модель с chain-of-thought
- 1M контекст, 384K max output

**🗣️ Русский язык:** ⭐⭐⭐⭐⭐ — DeepSeek отлично работает с русским языком. Модели обучены на мультилингвальных данных.

**⚡ Скорость:** Быстрая. V4 Flash оптимизирован для скорости.

**✅ Плюсы:**
- 5M бесплатных токенов при регистрации
- Самые низкие цены после бесплатных токенов
- Автоматическое контекстное кэширование
- OpenAI-совместимый API
- Огромный контекст (1M токенов)
- Off-peak скидки

**❌ Минусы:**
- Бесплатные токены истекают через 30 дней
- Иногда бывают перебои в работе (популярность вызывает перегрузки)
- Нет постоянного бесплатного tier после trial

**🔑 Как получить доступ:**
1. Зарегистрироваться на platform.deepseek.com
2. Получить 5M бесплатных токенов автоматически
3. Создать API ключ

**📌 Пример кода Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-YOUR_DEEPSEEK_KEY",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "Ты — помощник в Telegram. Отвечай на русском."},
        {"role": "user", "content": "Объясни разницу между REST API и WebSocket"}
    ],
    stream=False
)
print(response.choices[0].message.content)
```

---

### 10. Cerebras

**🔗 Ссылки:**
- Сайт: https://cerebras.ai
- Cloud: https://cloud.cerebras.ai
- API endpoint: `https://api.cerebras.ai/v1`

**💰 Стоимость / бесплатные лимиты:**
- **1,000,000 бесплатных токенов в день** — самый щедрый daily лимит!
- 5 RPM, 30K TPM
- Не требуется кредитная карта
- Developer tier: от $10, 10x лимиты

**🤖 Доступные модели:**
- `gpt-oss-120b` — OpenAI open-weight модель
- `zai-glm-4.7` — GLM модель
- `llama-4-scout` — 10M контекст
- `qwen3-235b-instruct` — 235B параметров

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Qwen3 отлично работает с русским. GPT-OSS тоже хорош.

**⚡ Скорость:** ⭐⭐⭐⭐⭐ — До 2,600 токенов/секунду! Wafer-scale чипы обеспечивают рекордную скорость.

**✅ Плюсы:**
- Самый щедрый бесплатный daily лимит (1M tokens)
- Рекордная скорость inference
- Не требует кредитной карты
- Большие модели (120B, 235B) бесплатно

**❌ Минусы:**
- Контекст ограничен 8,192 токенами на free tier
- Модельная линейка меняется
- Нет GPT/Claude моделей

**📌 Пример кода Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="csk-YOUR_CEREBRAS_KEY",
    base_url="https://api.cerebras.ai/v1"
)

response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Напиши стихотворение о зиме на русском языке"}
    ]
)
print(response.choices[0].message.content)
```

---

### 11. GitHub Models

**🔗 Ссылки:**
- Сайт: https://github.com/marketplace/models
- API endpoint: `https://models.github.ai/inference`

**💰 Стоимость / бесплатные лимиты:**
- **Бесплатно для всех GitHub пользователей**
- 10 RPM, 50-150 RPD (зависит от модели)
- 45+ моделей от разных провайдеров
- Не требуется кредитная карта

**🤖 Доступные модели:**
- GPT-5 (200K контекст)
- GPT-4.1, GPT-4o, o4-mini
- Llama-4 Scout/Maverick
- Mistral Small 3.1
- DeepSeek-R1

**🗣️ Русский язык:** ⭐⭐⭐⭐⭐ — GPT и Llama отлично работают с русским.

**⚡ Скорость:** Средняя

**✅ Плюсы:**
- Бесплатно для всех GitHub пользователей
- Доступ к GPT-5 без оплаты!
- OpenAI-совместимый API
- 45+ моделей под одним ключом

**❌ Минусы:**
- Ограниченные лимиты (50-150 RPD)
- Только для prototyping
- Нет гарантии доступности

**📌 Пример кода Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_GITHUB_TOKEN",
    base_url="https://models.github.ai/inference"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Привет! Расскажи о Python asyncio"}
    ]
)
print(response.choices[0].message.content)
```

---

### 12. Cloudflare Workers AI

**🔗 Ссылки:**
- Сайт: https://developers.cloudflare.com/workers-ai
- API endpoint: `https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/`

**💰 Стоимость / бесплатные лимиты:**
- **10,000 Neurons/день** бесплатно
- Распределённый edge inference (300+ дата-центров)
- Не требуется кредитная карта

**🤖 Доступные модели:**
- Llama 3.3 70B
- Mistral 7B
- DeepSeek models
- Kimi K2.5 (!)
- Whisper

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Llama и Mistral хорошо работают с русским.

**⚡ Скорость:** ⭐⭐⭐⭐⭐ — Edge inference, 10-50ms latency по всему миру.

**✅ Плюсы:**
- Глобальное edge распределение
- Kimi K2.5 доступен!
- Быстрый cold start
- Интеграция с Cloudflare Workers

**❌ Минусы:**
- Нужен Cloudflare аккаунт
- Меньше моделей чем у OpenRouter
- Не полностью OpenAI-совместимый

---

### 13. Perplexity API

**🔗 Ссылки:**
- Сайт: https://perplexity.ai
- API: https://docs.perplexity.ai

**💰 Стоимость / бесплатные лимиты:**
- **Нет бесплатного API tier.**
- Sonar API: $0.25/M input, $2.50/M output
- Search API: $5/1,000 запросов
- Pro подписчики ($20/мес) могут получать $5 API credits/мес

**🤖 Доступные модели:**
- `sonar` — базовый поиск + LLM
- `sonar-pro` — расширенный reasoning
- `sonar-deep-research` — глубокое исследование

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Хороший, но ориентирован на поиск на английском.

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Встроенный web search с цитатами
- Отлично для RAG-приложений
- Дешёвый input pricing

**❌ Минусы:**
- Нет бесплатного tier
- Per-request fees кроме token costs
- Не лучший выбор для чистого чат-бота

---

### 14. Together AI

**🔗 Ссылки:**
- Сайт: https://together.ai
- API endpoint: `https://api.together.xyz/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Нет бесплатного tier.** Минимальный депозит $5.
- Startup Accelerator: до $50K credits
- Llama 3.1 8B: ~$0.10/M input
- 200+ open-source моделей

**🤖 Доступные модели:**
- Llama, Mixtral, Qwen, Mistral
- Kimi K2.5 (через Together)
- Модели для fine-tuning

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Зависит от модели.

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Лучшая платформа для fine-tuning
- 200+ моделей
- Kimi K2.5 доступен

**❌ Минусы:**
- Нет бесплатного tier
- Минимум $5 для начала

---

## Локальные модели

---

### 15. Ollama

**🔗 Ссылки:**
- Сайт: https://ollama.com
- GitHub: https://github.com/ollama/ollama

**💰 Стоимость / бесплатные лимиты:**
- **Полностью бесплатно.** Нет никаких ограничений.
- Требуется GPU/RAM для запуска моделей
- Нет подписок, нет API-ключей

**🤖 Лучшие модели для Telegram-бота (с поддержкой русского):**
- `qwen3` / `qwen3:14b` — лучший баланс качества/скорости для русского
- `llama3.3` — хороший общий вариант
- `mistral` — быстрый, лёгкий
- `deepseek-r1:14b` — reasoning модель
- `gemma3:12b` — Google модель, мультимодальная
- `kimi-k2.6` — coding + agents (требует много VRAM)
- **Saiga** модели (русскоязычные fine-tunes, если доступны)

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Qwen3 и Llama 3.3 хорошо работают с русским. Для лучших результатов используйте модели 14B+ параметров.

**⚡ Скорость:** Зависит от оборудования:
- 7B модель: 6-8GB RAM/VRAM, ~20-40 токенов/сек
- 14B модель: 10-16GB RAM/VRAM, ~15-25 токенов/сек
- 70B модель: 42-48GB RAM/VRAM (Q4 квантизация)

**✅ Плюсы:**
- Полностью бесплатно и безлимитно
- Полная приватность — данные не уходят в облако
- Работает offline
- Простая установка и использование
- Огромный выбор моделей

**❌ Минусы:**
- Требует мощного оборудования
- Качество уступает облачным API (GPT-4o, Claude)
- Нужно самостоятельно обновлять модели
- Зависимость от железа для скорости

**🔑 Как получить доступ:**
1. Установить Ollama: https://ollama.com/download
2. Запустить модель: `ollama run qwen3:14b`
3. API доступен на `http://localhost:11434`

**📌 Пример кода Python:**
```python
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt, model="qwen3:14b"):
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "system": "Ты — полезный Telegram-бот. Всегда отвечай на русском языке.",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    })
    return response.json()["response"]

answer = ask_ollama("Что такое машинное обучение? Объясни простыми словами.")
print(answer)
```

**📌 Пример интеграции с Telegram-ботом:**
```python
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def ask_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": "qwen3:14b",
        "prompt": prompt,
        "system": "Ты — дружелюбный ассистент. Отвечай на русском языке.",
        "stream": False
    })
    return response.json()["response"]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот с локальной моделью AI. Задай мне любой вопрос!")

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("Думаю...")
    answer = ask_ollama(message.text)
    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 16. LM Studio

**🔗 Ссылки:**
- Сайт: https://lmstudio.ai

**💰 Стоимость / бесплатные лимиты:**
- **Бесплатно для личного использования.**
- Платная версия для коммерческого использования.

**🤖 Доступные модели:**
- Любые GGUF модели из HuggingFace
- Qwen3, Llama 3.3, Mistral, Gemma, DeepSeek R1
- Встроенный каталог моделей

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Зависит от выбранной модели. Qwen3 и Llama отлично работают с русским.

**⚡ Скорость:** Зависит от GPU

**✅ Плюсы:**
- GUI интерфейс (не нужен терминал)
- Встроенный chat интерфейс
- Встроенный сервер (OpenAI-compatible API)
- Легко переключать модели
- Поддержка vision моделей

**❌ Минусы:**
- Требует GPU
- Не для production server deployment
- GUI нужен для управления

**📌 Пример кода Python (используя встроенный API сервер LM Studio):**
```python
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",
    base_url="http://localhost:1234/v1"
)

response = client.chat.completions.create(
    model="local-model",  # Имя не важно, используется загруженная модель
    messages=[
        {"role": "system", "content": "Ты — ассистент на русском."},
        {"role": "user", "content": "Привет!"}
    ]
)
print(response.choices[0].message.content)
```

---

### 17. llama.cpp

**🔗 Ссылки:**
- GitHub: https://github.com/ggml-org/llama.cpp

**💰 Стоимость / бесплатные лимиты:**
- **Полностью бесплатно.** Open-source проект.

**🤖 Доступные модели:**
- Любые GGUF модели
- Поддержка Qwen, Llama, Mistral, Gemma, DeepSeek

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Зависит от модели.

**⚡ Скорость:** Зависит от железа. Оптимизирован для CPU и GPU.

**✅ Плюсы:**
- Максимальная производительность для локального inference
- Поддержка всех GPU (NVIDIA, AMD, Apple Silicon)
- Самый низкий уровень — максимальный контроль
- Поддержка квантизации (4-bit, 8-bit)

**❌ Минусы:**
- Только CLI — нет GUI
- Требует компиляции
- Более сложная настройка чем Ollama

**📌 Пример использования:**
```bash
# Клонировать репозиторий
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

# Скомпилировать с CUDA поддержкой
cmake -B build -DGGML_CUDA=ON -DBUILD_SHARED_LIBS=OFF
cmake --build build --config Release -j

# Запустить сервер
./build/bin/llama-server \
    -hf Qwen/Qwen3-14B-GGUF \
    --host 0.0.0.0 --port 8080
```

---

### 18. HuggingFace Inference API

**🔗 Ссылки:**
- Сайт: https://huggingface.co/docs/api-inference
- Serverless API: `https://api-inference.huggingface.co`

**💰 Стоимость / бесплатные лимиты:**
- **Несколько сотен запросов в час** на free tier
- Ограничение: модели <10B параметров
- Cold start 10-30 секунд на непопулярных моделях
- PRO ($9/мес): повышенные лимиты + ZeroGPU

**🤖 Доступные модели:**
- Тысячи open-source моделей
- Llama 3.2 8B, Qwen 2.5 7B, Mistral 7B
- Специализированные модели (NER, summarization, embeddings)

**🗣️ Русский язык:** ⭐⭐⭐ — Зависит от модели.

**⚡ Скорость:** Медленная (cold start)

**✅ Плюсы:**
- Огромный выбор моделей
- Не требует установки
- Не требует кредитной карты
- Инференс провайдеры (Groq, Together) доступны через HF

**❌ Минусы:**
- Cold start
- Rate limits
- Только модели <10B на free tier

**📌 Пример кода Python:**
```python
import requests

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen3-8B"
headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "Привет! Расскажи о себе.",
    "parameters": {"max_new_tokens": 250}
})
print(output[0]["generated_text"])
```

---

## Специализированные сервисы

---

### 19. SambaNova Cloud

**🔗 Ссылки:**
- Сайт: https://cloud.sambanova.ai
- API endpoint: `https://api.sambanova.ai/v1`

**💰 Стоимость / бесплатные лимиты:**
- **Бесплатный tier** + $5 начальных кредитов (30 дней)
- 20 RPM, 20 RPD, 200K tokens/day
- Не требуется кредитная карта
- OpenAI SDK-совместимый

**🤖 Доступные модели:**
- Llama 3.3 70B
- DeepSeek V3.1/V3.2
- GPT-OSS 120B
- Gemma 4 31B

**🗣️ Русский язык:** ⭐⭐⭐⭐ — Зависит от модели.

**⚡ Скорость:** Быстрая (RDU чипы)

**✅ Плюсы:**
- Бесплатный tier без карты
- Быстрый inference
- Начальные $5 кредиты

**❌ Минусы:**
- Ограниченный выбор моделей
- Низкие RPD (20)

**📌 Пример кода Python:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_SAMBANOVA_KEY",
    base_url="https://api.sambanova.ai/v1"
)

response = client.chat.completions.create(
    model="Meta-Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "Привет!"}]
)
print(response.choices[0].message.content)
```

---

### 20. Fireworks AI

**🔗 Ссылки:**
- Сайт: https://fireworks.ai

**💰 Стоимость / бесплатные лимиты:**
- $1 free credit при регистрации
- 10 RPM без оплаты

**🤖 Доступные модели:**
- Llama 3.1 70B/405B
- Mixtral 8x22B
- Специализация на structured output / function calling

**🗣️ Русский язык:** ⭐⭐⭐⭐

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Лучший для function calling
- Structured output
- FireFunction v2

**❌ Минусы:**
- $1 credit — очень мало
- Нет постоянного free tier

---

### 21. xAI (Grok)

**🔗 Ссылки:**
- Сайт: https://x.ai

**💰 Стоимость / бесплатные лимиты:**
- $25 signup credit
- $150/мес дополнительно через data sharing программу
- Нет постоянного free tier

**🤖 Доступные модели:**
- Grok 4.1 Fast — 2M контекст!

**🗣️ Русский язык:** ⭐⭐⭐⭐

**⚡ Скорость:** Быстрая

**✅ Плюсы:**
- Огромный контекст (2M токенов)
- Интеграция с X (Twitter)

**❌ Минусы:**
- Кредиты истекают
- Дорогой после trial

---

## Итоговая рекомендация: Лучшие 3 варианта для Telegram-бота

---

### 🥇 Вариант 1: OpenRouter (бесплатно, 0$)

**Идеально для:** Начинающих разработчиков, тестирования, небольших ботов.

**Стратегия:**
- Используйте бесплатные модели с суффиксом `:free`
- Ротация моделей для обхода лимитов
- Для лучшего русского: `qwen/qwen3-235b-a22b:free` или `deepseek/deepseek-r1:free`

**Лимиты:** 20 RPM, 50-200 RPD (покупка $10 даёт 1,000 RPD)

**Пример ротации моделей:**
```python
FREE_MODELS = [
    "qwen/qwen3-235b-a22b:free",          # Лучший русский
    "deepseek/deepseek-r1:free",           # Лучший reasoning
    "meta-llama/llama-3.3-70b-instruct:free", # Общие задачи
    "meta-llama/llama-4-scout:free",        # Огромный контекст
]
```

---

### 🥈 Вариант 2: DeepSeek API (5M бесплатных токенов)

**Идеально для:** Разработки, прототипирования, ботов с умеренной нагрузкой.

**Стратегия:**
- 5M бесплатных токенов на 30 дней (~$8 стоимости)
- После — самые низкие цены на рынке
- Используйте V4 Flash для экономии

**Стоимость после бесплатных токенов:** ~$0.14-0.28 за 1M токенов

---

### 🥉 Вариант 3: Groq API (полностью бесплатно)

**Идеально для:** Ботов, требующих мгновенных ответов.

**Стратегия:**
- Полностью бесплатный tier
- Самая высокая скорость inference
- Llama 4 Scout с 10M контекстом бесплатно
- Qwen3 для отличного русского языка

**Лимиты:** 30 RPM, 1,000 RPD (Llama 70B)

---

### 🏆 Бонус: Стратегия "Комбинированная" (максимум бесплатного)

Для production Telegram-бота рекомендуется комбинировать несколько провайдеров:

```python
# Маршрутизация запросов между несколькими free tiers
async def get_ai_response(prompt):
    providers = [
        # Приоритет: Groq (самый быстрый)
        {"name": "groq", "model": "llama-3.3-70b-versatile", "weight": 3},
        # Fallback 1: Cerebras (самый щедрый daily лимит)
        {"name": "cerebras", "model": "gpt-oss-120b", "weight": 2},
        # Fallback 2: Gemini (много запросов в день)
        {"name": "gemini", "model": "gemini-2.5-flash", "weight": 2},
        # Fallback 3: OpenRouter (много моделей)
        {"name": "openrouter", "model": "deepseek/deepseek-r1:free", "weight": 1},
    ]
    # Реализуйте round-robin с fallback
    ...
```

**Ожидаемый бюджет:**
- На 1,000 запросов/день: **$0/месяц** (используя только free tiers)
- На 10,000 запросов/день: **$0-5/месяц** (Groq + Gemini + Cerebras)
- На 100,000+ запросов/день: **$10-50/месяц** (DeepSeek V4 Flash)

---

### 📊 Сравнение качества ответов на русском языке

| API | Русский язык | Качество общих ответов | Код | Рекомендация |
|-----|-------------|----------------------|-----|-------------|
| OpenAI GPT-4o | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Лучшее качество, но платно |
| Claude Sonnet 4.6 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Лучший reasoning, но платно |
| **DeepSeek V4** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Лучшее качество/цена** |
| **Kimi K2.5** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Отличный, дешёвый |
| **Qwen3 (Groq)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Лучший бесплатный русский** |
| **Gemini 2.5 Flash** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Самый щедрый free tier** |
| Llama 3.3 70B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Хороший бесплатный вариант |
| Mistral Large 3 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Дёшево, GDPR |
| Cohere Command R | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Только для RAG |

---

### ⚠️ Важные замечания

1. **Бесплатные tiers изменяются.** Провайдеры регулярно меняют лимиты. Google, например, в конце 2025 резко сократил бесплатные квоты Gemini.

2. **Ротация ключей.** Для production рекомендуется иметь fallback-провайдеры.

3. **Rate limiting.** Всегда обрабатывайте 429 ошибки и добавляйте exponential backoff.

4. **Data privacy.** Некоторые бесплатные tiers используют данные для обучения моделей. Для sensitive данных используйте локальные модели (Ollama) или paid tiers.

5. **Русский язык.** Лучшие бесплатные модели для русского: Qwen3 (Groq), DeepSeek R1 (OpenRouter), Llama 3.3 (Groq/OpenRouter).

6. **Kimi API** — отличный выбор для русского языка, но требует минимум $1. Если готовы заплатить $1 — это один из лучших вариантов по соотношению цена/качество.

---

### 📚 Полезные ресурсы

- [Awesome Free LLM APIs](https://github.com/mnfst/awesome-free-llm-apis) — обновляемый список бесплатных API
- [Price Per Token](https://pricepertoken.com) — сравнение цен всех провайдеров
- [Free LLM APIs 2026 Guide](https://klymentiev.com/blog/free-llm-api) — подробный гайд
- [OpenRouter Models](https://openrouter.ai/models) — список всех моделей с ценами

---

*Исследование проведено в июле 2026 года. Информация актуальна на момент написания, но провайдеры могут изменять условия.*
