# Бесплатные API новостей -- Исследование 2025-2026

> **Дата исследования:** Июль 2026
> **Цель:** Подбор оптимальных бесплатных источников новостей для Telegram-бота, присылающего краткую утреннюю сводку на русском языке
> **Ключевые критерии:** Поддержка русского языка, стабильность, легкость интеграции, легальность использования

---

## Сравнительная таблица

| API | Бесплатный лимит | Русский язык | Источники | Фильтрация | API-ключ | Задержка | Рейтинг |
|-----|-------------------|--------------|-----------|------------|----------|----------|---------|
| **NewsAPI.org** | 100 запросов/день | ✅ Да (14 языков) | 150,000+ | Категория, страна, язык, дата, ключевые слова | ✅ Да | 24 часа (free) | ★★★☆☆ |
| **Currents API** | 1,000 запросов/день | ✅ Да (20+ языков) | 120,000+ | Категория, страна, язык, дата, ключевые слова | ✅ Да | Реальное время | ★★★★★ |
| **GNews API** | 100 запросов/день | ✅ Да (41 язык) | 80,000+ | Категория, страна, язык, дата, ключевые слова | ✅ Да | Реальное время | ★★★★☆ |
| **NewsData.io** | 200 кредитов/день (~60-80 запросов) | ✅ Да (89 языков!) | 97,000+ | Язык, страна, категория, дата, ключевые слова | ✅ Да | 12 часов (free) | ★★★★☆ |
| **The Guardian API** | 5,000 запросов/день | ❌ Только английский | 1 (The Guardian) | Секция, тег, дата, ключевые слова | ✅ Да | Реальное время | ★★☆☆☆ |
| **NYTimes API** | 500 запросов/день | ❌ Только английский | 1 (NYTimes) | Секция, дата, ключевые слова | ✅ Да | Реальное время | ★★☆☆☆ |
| **MediaStack** | 100 запросов/месяц | ✅ Да (13 языков) | 7,500+ | Категория, страна, язык, ключевые слова | ✅ Да | Близко к реальному | ★☆☆☆☆ |
| **RSS-фиды** | Без лимитов | ✅ Да (полный контент) | Зависит от фида | Нет встроенной | ❌ Нет | Реальное время | ★★★★★ |
| **Google News RSS** | Без лимитов (неофициально) | ✅ Да | Google News | Поисковый запрос, язык, страна | ❌ Нет | Реальное время | ★★★★☆ |

---

## Детальный обзор каждого API

---

### 1. NewsAPI (newsapi.org) ⭐ Самый известный

**Ссылка:** https://newsapi.org  
**Документация:** https://newsapi.org/docs

#### Лимиты бесплатного тарифа (Developer)
- **100 запросов в день**
- Максимум 20 статей на запрос (всего до 2,000 статей/день)
- **Задержка статей 24 часа** на бесплатном тарифе
- **Только для разработки** (development use only) -- запрещено коммерческое использование
- Нет CORS для production (localhost only)

#### Поддержка русского языка
- ✅ **Да**, код языка: `ru`
- 14 языков всего (en, de, es, fr, he, it, nl, no, pt, ru, sv, ud, zh)
- Поддержка страны: `ru` для России
- **Проблема:** На бесплатном тарифе новости с 24-часовой задержкой, что не подходит для утренней сводки

#### Источники новостей
- 150,000+ источников и блогов по всему миру
- Включает крупные российские и международные СМИ

#### Фильтрация
- По категориям: business, entertainment, general, health, science, sports, technology
- По стране (2-буквенный ISO код)
- По языку
- По источникам
- По дате публикации (from, to)
- По ключевым словам (q)
- Сортировка: relevancy, popularity, publishedAt

#### Формат ответа (JSON)
```json
{
  "status": "ok",
  "totalResults": 2,
  "articles": [
    {
      "source": {"id": "lenta", "name": "Lenta"},
      "author": "Author Name",
      "title": "Заголовок новости",
      "description": "Описание новости",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "publishedAt": "2025-01-01T12:00:00Z",
      "content": "Краткое содержание статьи..."
    }
  ]
}
```

#### Пример кода на Python
```python
import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"

def get_russian_news_newsapi():
    """Получение новостей на русском языке через NewsAPI"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "ru",         # Россия
        "language": "ru",        # Русский язык
        "category": "general",   # Общие новости
        "pageSize": 10,          # Количество статей
        "apiKey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] == "ok":
        articles = data["articles"]
        news_list = []
        for article in articles:
            news_list.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "published": article["publishedAt"],
                "source": article["source"]["name"]
            })
        return news_list
    else:
        print(f"Ошибка: {data.get('message', 'Unknown error')}")
        return []

# Использование
news = get_russian_news_newsapi()
for item in news:
    print(f"[{item['source']}] {item['title']}")
```

#### Плюсы
- ✅ Очень простой REST API
- ✅ Отличная документация
- ✅ Большое количество источников (150K+)
- ✅ Поддержка русского языка
- ✅ SDK для Python: `newsapi-python`

#### Минусы
- ❌ **24-часовая задержка** на бесплатном тарифе -- критично для утренней сводки
- ❌ Запрещено коммерческое использование на free tier
- ❌ Только localhost на бесплатном тарифе
- ❌ Всего 100 запросов/день
- ❌ **Не рекомендуется для production Telegram-бота**

#### Требования
- Регистрация на newsapi.org
- API-ключ (бесплатно)

---

### 2. Currents API ⭐ Лучший бесплатный тариф

**Ссылка:** https://currentsapi.services  
**Документация:** https://currentsapi.services/en/docs

#### Лимиты бесплатного тарифа
- **1,000 запросов в день**
- Без указания кредитной карты
- Коммерческое использование **разрешено**
- CORS: any-origin (можно использовать в production)
- Реальное время, без задержки
- 22,000+ источников

#### Поддержка русского языка
- ✅ **Да**, параметр `language`: `ru`
- 20+ языков поддерживается
- 70+ стран
- Отличное покрытие российских СМИ

#### Источники новостей
- 120,000+ источников
- 70+ стран
- 20+ языков
- 90K+ статей добавляется ежедневно
- 26M+ статей в архиве

#### Фильтрация
- По языку (`language`)
- По стране (`country`)
- По категории (`category`): regional, business, technology, entertainment, sports, science, health
- По ключевым словам (`keywords`)
- По дате (`start_date`, `end_date`)
- Пагинация через `page`

#### Формат ответа (JSON)
```json
{
  "status": "ok",
  "news": [
    {
      "id": "unique-id",
      "title": "Заголовок новости",
      "description": "Описание",
      "url": "https://example.com",
      "author": "Author",
      "image": "https://example.com/image.jpg",
      "language": "ru",
      "category": ["business"],
      "published": "2025-01-01 12:00:00 +0000"
    }
  ],
  "page": 1,
  "count": 10
}
```

#### Пример кода на Python
```python
import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_CURRENTS_API_KEY"

def get_russian_news_currents():
    """Получение новостей через Currents API"""
    url = "https://api.currentsapi.services/v1/latest-news"
    params = {
        "language": "ru",           # Русский язык
        "apiKey": API_KEY,
        "category": "general",
        "page_size": 10
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("status") == "ok":
        articles = data.get("news", [])
        news_list = []
        for article in articles:
            news_list.append({
                "title": article["title"],
                "description": article.get("description", ""),
                "url": article["url"],
                "published": article["published"],
                "source": article.get("author", "Unknown"),
                "image": article.get("image", None)
            })
        return news_list
    return []

# Использование
news = get_russian_news_currents()
for item in news:
    print(f"📰 {item['title']}\n   {item['description'][:100]}...\n")
```

#### Плюсы
- ✅ **Самый щедрый бесплатный тариф** (1,000 запросов/день)
- ✅ **Реальное время**, без задержки
- ✅ Коммерческое использование разрешено
- ✅ CORS any-origin -- можно в production
- ✅ Без кредитной карты
- ✅ Большое количество источников
- ✅ Поддержка русского языка

#### Минусы
- ❌ Базовые метаданные без NLP-обогащения (нет сентимента, сущностей)
- ❌ Категории грубые (news/business/tech/etc.)
- ❌ Меньше известен, меньше community

#### Требования
- Регистрация на currentsapi.services
- API-ключ (бесплатно, без карты)

---

### 3. GNews API

**Ссылка:** https://gnews.io  
**Документация:** https://gnews.io/docs/v4

#### Лимиты бесплатного тарифа
- **100 запросов в день**
- Максимум 10 статей на запрос
- API-ключ: бесплатный
- Коммерческое использование: разрешено
- Реальное время

#### Поддержка русского языка
- ✅ **Да**, параметр `lang`: `ru`
- 41 язык поддерживается
- 71 страна
- Поддержка поиска на русском языке

#### Источники новостей
- 80,000+ источников
- Быстрый ответ: 100-300 мс

#### Фильтрация
- По языку (`lang`)
- По стране (`country`): 71 страна
- По категории (`category`): general, world, nation, business, technology, entertainment, sports, science, health
- По ключевым словам (`q`)
- По дате (`from`, `to`)
- По источнику (`in` -- title, description, content)
- Пагинация через `max` и `page`

#### Формат ответа (JSON)
```json
{
  "totalArticles": 23456,
  "articles": [
    {
      "title": "Заголовок",
      "description": "Описание новости",
      "content": "Содержимое...",
      "url": "https://example.com",
      "image": "https://example.com/image.jpg",
      "publishedAt": "2025-01-01T12:00:00Z",
      "source": {
        "name": "Source Name",
        "url": "https://source.com"
      }
    }
  ]
}
```

#### Пример кода на Python
```python
import requests

API_KEY = "YOUR_GNEWS_API_KEY"

def get_russian_news_gnews():
    """Получение новостей через GNews API"""
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "lang": "ru",              # Русский язык
        "country": "ru",          # Россия
        "category": "general",   # Общие новости
        "max": 10,               # Количество статей
        "apikey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    articles = data.get("articles", [])
    news_list = []
    for article in articles:
        news_list.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "published": article["publishedAt"],
            "source": article["source"]["name"]
        })
    return news_list

# Использование
news = get_russian_news_gnews()
for item in news:
    print(f"📰 [{item['source']}] {item['title']}")
    print(f"   {item['description'][:120]}...")
    print(f"   Ссылка: {item['url']}\n")
```

#### Плюсы
- ✅ Реальное время
- ✅ Коммерческое использование разрешено
- ✅ Быстрый ответ (100-300 мс)
- ✅ 41 язык, включая русский
- ✅ Простой REST API
- ✅ Чистый JSON

#### Минусы
- ❌ Всего 100 запросов/день (как NewsAPI)
- ❌ Только 10 статей на запрос
- ❌ Нет NLP-обогащения
- ❌ Платный входной план от EUR 49.99/мес

#### Требования
- Регистрация на gnews.io
- API-ключ (бесплатно)

---

### 4. NewsData.io

**Ссылка:** https://newsdata.io  
**Документация:** https://newsdata.io/documentation

#### Лимиты бесплатного тарифа
- **200 API-кредитов в день**
- 10 статей на кредит (итого ~2,000 статей/день)
- **Задержка 12 часов** на бесплатном тарифе
- Коммерческое использование: **разрешено**
- Лимит: 30 кредитов каждые 15 минут
- Лимит символов в запросе: 100 символов (free)

#### Поддержка русского языка
- ✅ **Да**, код языка: `ru`
- **89 языков** -- лучшее языковое покрытие среди всех API
- 206 стран
- Отличный выбор для мультиязычных проектов

#### Источники новостей
- 97,000+ источников
- 206 стран
- 89 языков

#### Фильтрация
- По языку (`language`)
- По стране (`country`) -- до 5 стран за запрос
- По категории (`category`): top, sports, technology, business, science, entertainment, health, politics, food, travel
- По ключевым словам (`q`, `qInTitle`, `qInMeta`)
- По дате (`from_date`, `to_date`, `timeframe`)
- По типу данных (`datatype`): news, blog, multimedia, forum, press_release, review, research, opinion, analysis, podcast
- Исключение дубликатов (`removeduplicate`)
- Сортировка: pubdateasc, relevancy, source, fetched_at

#### Формат ответа (JSON)
```json
{
  "status": "success",
  "totalResults": 550,
  "results": [
    {
      "article_id": "unique_id",
      "title": "Заголовок новости",
      "link": "https://example.com",
      "keywords": ["keyword1", "keyword2"],
      "creator": ["Author Name"],
      "description": "Описание",
      "content": "Содержимое...",
      "pubDate": "2025-01-01 12:00:00",
      "pubDateTZ": "UTC",
      "image_url": "https://example.com/image.jpg",
      "source_id": "source_name",
      "source_name": "Source Name",
      "source_url": "https://source.com",
      "language": "russian",
      "country": ["russia"],
      "category": ["top"]
    }
  ],
  "nextPage": "NEXT_PAGE_TOKEN"
}
```

#### Пример кода на Python
```python
import requests

API_KEY = "YOUR_NEWSDATA_API_KEY"

def get_russian_news_newsdata():
    """Получение новостей через NewsData.io"""
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": API_KEY,
        "language": "ru",           # Русский язык
        "country": "ru",           # Россия
        "category": "top",         # Топ-новости
        "size": 10,                # Количество статей
        "removeduplicate": 1       # Удалить дубликаты
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("status") == "success":
        articles = data.get("results", [])
        news_list = []
        for article in articles:
            news_list.append({
                "title": article["title"],
                "description": article.get("description", ""),
                "url": article["link"],
                "published": article.get("pubDate", ""),
                "source": article.get("source_name", "Unknown"),
                "image": article.get("image_url", None)
            })
        return news_list
    return []

# Использование
news = get_russian_news_newsdata()
for item in news:
    print(f"📰 {item['title']}\n   Источник: {item['source']}\n")
```

#### Плюсы
- ✅ **Лучшее языковое покрытие** (89 языков)
- ✅ Коммерческое использование разрешено
- ✅ Большое количество источников (97K+)
- ✅ Отличная фильтрация
- ✅ Удаление дубликатов
- ✅ Поддержка множества типов контента

#### Минусы
- ❌ **12-часовая задержка** на free tier (лучше чем NewsAPI, но всё же)
- ❌ Система кредитов (200 кредитов = ~60-80 реальных запросов)
- ❌ Лимит 100 символов в поисковом запросе
- ❌ Дорогой входной платный тариф: $199.99/мес

#### Требования
- Регистрация на newsdata.io
- API-ключ (бесплатно)

---

### 5. The Guardian Open Platform API

**Ссылка:** https://open-platform.theguardian.com  
**Документация:** https://open-platform.theguardian.com/documentation

#### Лимиты бесплатного тарифа
- **5,000 запросов в день**
- **12 запросов в секунду**
- Developer tier -- только некоммерческое использование
- Требуется атрибуция

#### Поддержка русского языка
- ❌ **Нет** -- только английский контент The Guardian

#### Источники новостей
- Только The Guardian (с 1999 года)
- 2.4M+ элементов контента

#### Фильтрация
- По секции (section)
- По тегу (tag)
- По дате (from-date, to-date)
- По ключевым словам (q)
- По автору (byline)

#### Пример кода на Python
```python
import requests

API_KEY = "YOUR_GUARDIAN_API_KEY"

def get_guardian_news():
    """Получение новостей The Guardian"""
    url = "https://content.guardianapis.com/search"
    params = {
        "api-key": API_KEY,
        "q": "Russia",            # Поиск по России
        "section": "world",
        "page-size": 10,
        "show-fields": "headline,trailText",
        "order-by": "newest"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    articles = data.get("response", {}).get("results", [])
    news_list = []
    for article in articles:
        news_list.append({
            "title": article["webTitle"],
            "url": article["webUrl"],
            "published": article["webPublicationDate"],
            "section": article["sectionName"]
        })
    return news_list
```

#### Плюсы
- ✅ Очень высокое качество журналистики
- ✅ Большой архив с 1999 года
- ✅ Щедрые лимиты (5,000/день)
- ✅ Бесплатно для некоммерческого использования

#### Минусы
- ❌ **Нет русского языка** -- только английский
- ❌ **Только The Guardian** -- один источник
- ❌ Некоммерческое использование only

#### Требования
- Регистрация на open-platform.theguardian.com
- API-ключ (бесплатно)

---

### 6. New York Times API

**Ссылка:** https://developer.nytimes.com  
**Документация:** https://developer.nytimes.com/docs

#### Лимиты бесплатного тарифа
- **500 запросов в день** (Article Search API)
- Регистрация обязательна
- Требуется атрибуция "Data provided by The New York Times"

#### Поддержка русского языка
- ❌ **Нет** -- только английский контент

#### Источники новостей
- Только New York Times

#### API Endpoints
- Article Search API
- Top Stories API
- Most Popular API
- Times Wire API

#### Пример кода на Python
```python
import requests

API_KEY = "YOUR_NYT_API_KEY"

def get_nyt_news():
    """Получение новостей через NYTimes API"""
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": "Russia",
        "api-key": API_KEY,
        "page": 0,
        "sort": "newest"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    articles = data.get("response", {}).get("docs", [])
    news_list = []
    for article in articles:
        news_list.append({
            "title": article["headline"]["main"],
            "abstract": article.get("abstract", ""),
            "url": article["web_url"],
            "published": article["pub_date"],
            "section": article["section_name"]
        })
    return news_list
```

#### Плюсы
- ✅ Высокое качество данных
- ✅ Доступ к архиву
- ✅ Хорошая документация

#### Минусы
- ❌ **Нет русского языка**
- ❌ Только NYTimes контент
- ❌ Ограниченное использование

#### Требования
- Регистрация на developer.nytimes.com
- API-ключ (бесплатно)

---

### 7. MediaStack

**Ссылка:** https://mediastack.com  
**Документация:** https://mediastack.com/documentation

#### Лимиты бесплатного тарифа
- **100 запросов в месяц** (~3 запроса в день!)
- HTTPS только на платных тарифах
- Очень ограниченные данные

#### Поддержка русского языка
- ✅ **Да**, 13 языков
- 50+ стран
- 7,500+ источников

#### Фильтрация
- Страна, категория, язык, ключевые слова, дата

#### Пример кода на Python
```python
import requests

API_KEY = "YOUR_MEDIASTACK_API_KEY"

def get_news_mediastack():
    """Получение новостей через MediaStack"""
    url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": API_KEY,
        "languages": "ru",
        "countries": "ru",
        "limit": 10
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    articles = data.get("data", [])
    return [{
        "title": a["title"],
        "url": a["url"],
        "published": a["published_at"],
        "source": a["source"]
    } for a in articles]
```

#### Плюсы
- ✅ Самый дешевый платный тариф ($24.99/мес)
- ✅ Простой REST API
- ✅ Поддержка русского

#### Минусы
- ❌ **100 запросов в месяц** -- катастрофически мало
- ❌ HTTP только на free tier (не HTTPS)
- ❌ Нет NLP-обогащения
- ❌ Мало источников (7,500 vs 100K+ у конкурентов)
- ❌ **Не рекомендуется для Telegram-бота**

---

### 8. RSS-фиды -- Бесплатная альтернатива API ⭐ Рекомендуется

RSS (Really Simple Syndication) -- это формат веб-каналов, который позволяет получать обновления сайтов в стандартизированном виде. Большинство новостных сайтов предоставляют RSS-ленты бесплатно.

#### Лимиты
- **Без ограничений** -- вы сами контролируете частоту запросов
- Рекомендуется разумная частота (каждые 10-30 минут)
- Нужно уважать `robots.txt` и не нагружать серверы

#### Поддержка русского языка
- ✅ **Да**, полный контент на русском языке
- Новости напрямую от российских СМИ

#### RSS-ленты российских СМИ

| Источник | RSS URL | Описание |
|----------|---------|----------|
| **РИА Новости** | `https://ria.ru/export/rss2/index.xml` | Все новости РИА |
| **РИА Новости (Главное)** | `https://ria.ru/export/rss2/archive/index.xml` | Главные новости |
| **ТАСС** | `https://tass.ru/rss/v2.xml` | Все новости ТАСС |
| **ТАСС (English)** | `https://tass.com/rss/v2.xml` | ТАСС на английском |
| **Лента.ру** | `https://lenta.ru/rss/news` | Все новости Ленты |
| **РБК** | `https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss` | Главные новости РБК |
| **РБК (Экономика)** | `https://rssexport.rbc.ru/rbcnews/economics/30/rsslite.rss` | Экономика |
| **Коммерсант** | `https://www.kommersant.ru/RSS/news.xml` | Новости Коммерсанта |
| **Ведомости** | `https://www.vedomosti.ru/rss/news` | Новости Ведомостей |
| **Известия** | `https://iz.ru/xml/rss/all.xml` | Все новости Известий |
| **RT (Russia Today)** | `https://rt.com/rss` | RT на английском |
| **RT на русском** | `https://russian.rt.com/rss` | RT на русском |
| **Интерфакс** | `https://www.interfax.ru/rss.asp` | Интерфакс |
| **Хабр** | `https://habr.com/ru/rss/all/all/?fl=ru` | Все посты Хабра (рус.) |
| **Хабр (Топ)** | `https://habr.com/ru/rss/top/daily/?fl=ru` | Топ посты за день |
| **Google News (RU)** | `https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru` | Главные новости Google |
| **Google News поиск** | `https://news.google.com/rss/search?q=QUERY&hl=ru&gl=RU&ceid=RU:ru` | Поисковый запрос |

#### Пример кода на Python с feedparser

```python
import feedparser
from datetime import datetime

# RSS-ленты российских СМИ
RSS_FEEDS = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
    "Коммерсант": "https://www.kommersant.ru/RSS/news.xml",
    "Ведомости": "https://www.vedomosti.ru/rss/news",
    "Известия": "https://iz.ru/xml/rss/all.xml",
}

def parse_rss_feed(feed_url, source_name, limit=5):
    """Парсинг RSS-ленты новостей"""
    feed = feedparser.parse(feed_url)
    articles = []
    
    for entry in feed.entries[:limit]:
        article = {
            "title": entry.get("title", "Без заголовка"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "source": source_name
        }
        articles.append(article)
    
    return articles

def get_all_russian_news():
    """Получение новостей со всех источников"""
    all_news = []
    
    for source_name, feed_url in RSS_FEEDS.items():
        try:
            articles = parse_rss_feed(feed_url, source_name, limit=3)
            all_news.extend(articles)
            print(f"✅ {source_name}: получено {len(articles)} статей")
        except Exception as e:
            print(f"❌ Ошибка при получении {source_name}: {e}")
    
    # Сортировка по дате публикации (если доступна)
    all_news.sort(key=lambda x: x["published"], reverse=True)
    
    return all_news

# Использование
news = get_all_russian_news()
print(f"\n📊 Всего получено новостей: {len(news)}\n")

for item in news[:10]:
    print(f"📰 [{item['source']}] {item['title']}")
    print(f"   📝 {item['summary'][:150]}...")
    print(f"   🔗 {item['link']}\n")
```

#### Пример формирования утренней сводки для Telegram

```python
def format_morning_digest(articles, max_articles=10):
    """Формирование утренней сводки новостей для Telegram"""
    from datetime import datetime
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    digest = f"🌅 <b>Утренняя сводка новостей</b>\n"
    digest += f"📅 {today}\n"
    digest += "━" * 25 + "\n\n"
    
    # Группировка по источникам
    by_source = {}
    for article in articles[:max_articles]:
        source = article["source"]
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(article)
    
    for source, items in by_source.items():
        digest += f"📍 <b>{source}</b>\n"
        for item in items:
            # Очистка HTML-тегов из заголовка
            title = item["title"].replace("<", "&lt;").replace(">", "&gt;")
            digest += f"  • {title}\n"
        digest += "\n"
    
    digest += "━" * 25 + "\n"
    digest += "🔗 <i>Подробнее по ссылкам в заголовках</i>"
    
    return digest

# Формирование дайджеста
digest = format_morning_digest(news)
print(digest)
```

#### Плюсы
- ✅ **Полностью бесплатно**
- ✅ **Без ограничений** на количество запросов
- ✅ **Полный контент** на русском языке
- ✅ **Реальное время** обновлений
- ✅ **Прямые ссылки** на оригинальные статьи
- ✅ **Легальность** -- RSS предназначен для агрегации
- ✅ **Не требует API-ключей**
- ✅ **Работает без интернета** (после загрузки)

#### Минусы
- ❌ Нет единого формата (некоторые фиды могут отличаться)
- ❌ Нужно следить за работоспособностью фидов
- ❌ Нет встроенной фильтрации
- ❌ HTML-теги в summary могут требовать очистки
- ❌ Некоторые сайты могут ограничивать или отключать RSS

#### Рекомендации по использованию RSS
1. **Кэшируйте результаты** -- не запрашивайте чаще раз в 10-15 минут
2. **Дедуплицируйте новости** -- одинаковые новости могут появляться в разных фидах
3. **Очищайте HTML** -- используйте `html.parser` или регулярные выражения
4. **Обрабатывайте ошибки** -- фиды могут быть временно недоступны
5. **Уважайте robots.txt**

---

### 9. Google News RSS (неофициальный) ⭐ Отличная альтернатива

Google News предоставляет RSS-ленты, хотя и не документированы официально. Это мощный способ получать новости по поисковым запросам.

#### URL-шаблоны Google News RSS

| Тип | URL |
|-----|-----|
| **Главные новости (RU)** | `https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru` |
| **Топ по теме (технологии)** | `https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ru&gl=RU&ceid=RU:ru` |
| **Поиск по ключевому слову** | `https://news.google.com/rss/search?q=python&hl=ru&gl=RU&ceid=RU:ru` |
| **Поиск с фильтром по времени** | `https://news.google.com/rss/search?q=python+when:24h&hl=ru&gl=RU&ceid=RU:ru` |
| **Поиск по сайту** | `https://news.google.com/rss/search?q=site:ria.ru&hl=ru&gl=RU&ceid=RU:ru` |

#### Поддерживаемые темы
`WORLD`, `NATION`, `BUSINESS`, `TECHNOLOGY`, `ENTERTAINMENT`, `SCIENCE`, `SPORTS`, `HEALTH`

#### Пример кода на Python

```python
import feedparser
import re
from html.parser import HTMLParser

def get_google_news_ru(query=None, topic=None, max_results=10):
    """
    Получение новостей через Google News RSS
    
    :param query: Поисковый запрос (например, "экономика россии")
    :param topic: Тема (TECHNOLOGY, BUSINESS, WORLD и т.д.)
    :param max_results: Максимальное количество результатов
    """
    if query:
        # URL-кодирование запроса
        encoded_query = query.replace(" ", "%20")
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ru&gl=RU&ceid=RU:ru"
    elif topic:
        url = f"https://news.google.com/rss/headlines/section/topic/{topic}?hl=ru&gl=RU&ceid=RU:ru"
    else:
        url = "https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru"
    
    feed = feedparser.parse(url)
    
    articles = []
    for entry in feed.entries[:max_results]:
        # Очистка HTML-тегов из описания
        description = re.sub(r'<[^>]+>', '', entry.get("summary", ""))
        
        articles.append({
            "title": entry.get("title", "Без заголовка"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "description": description,
            "source": entry.get("source", {}).get("title", "Google News")
            if hasattr(entry.get("source", {}), "get") else "Google News"
        })
    
    return articles

# Примеры использования
print("=== Главные новости России ===")
news = get_google_news_ru(max_results=5)
for item in news:
    print(f"📰 {item['title']}\n")

print("=== Новости технологий ===")
tech_news = get_google_news_ru(topic="TECHNOLOGY", max_results=5)
for item in tech_news:
    print(f"💻 {item['title']}\n")

print('=== Поиск: "экономика России" ===')
search_news = get_google_news_ru(query="экономика России", max_results=5)
for item in search_news:
    print(f"📊 {item['title']}\n")
```

#### Плюсы
- ✅ **Бесплатно и без лимитов**
- ✅ **Агрегация** множества источников
- ✅ **Поиск по ключевым словам**
- ✅ **Фильтрация по времени** (`when:1h`, `when:24h`, `when:7d`)
- ✅ **Фильтрация по языку и стране**
- ✅ **Не требует API-ключа**

#### Минусы
- ❌ Неофициальный/недокументированный API
- ❌ Google может изменить URL-формат
- ❌ Ссылки через редирект Google (нужно обрабатывать)
- ❌ Нет гарантий стабильности

---

### 10. Парсинг новостей напрямую (Web Scraping) ⚠️ Осторожно

**Важно:** Прямой парсинг сайтов без разрешения может нарушать:
- Условия использования (Terms of Service)
- Авторские права
- Законы о защите данных (GDPR в ЕС)

#### Правовые аспекты (2025-2026)

| Регион | Публичные данные | PII/персональные данные | Контент за paywall |
|--------|------------------|-------------------------|-------------------|
| **США** | ✅ Обычно легально | ⚠️ Законы штатов | 🔴 Риск CFAA |
| **ЕС/UK** | ✅ Легально (TDM exception) | 🔴 GDPR | 🔴 Уголовная ответственность |
| **Россия** | ✅ Легально для личного использования | ⚠️ 152-ФЗ | ⚠️ Зависит от ToS |

**Правила безопасного парсинга:**
1. ✅ Парсить **только публично доступные** данные
2. ✅ **Не обходить** авторизацию, CAPTCHA, paywall
3. ✅ Соблюдать `robots.txt`
4. ✅ Использовать разумные задержки между запросами (1-3 секунды)
5. ✅ Указывать User-Agent с контактной информацией
6. ✅ Не хранить полный текст статей (копирайт)
7. ✅ **Хранить только заголовки, даты, ссылки** (метаданные)

#### Пример (только для образовательных целей)

```python
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "NewsBot/1.0 (your@email.com) - Educational purposes"
}

def scrape_with_caution(url):
    """
    ⚠️ Используйте только если:
    1. Сайт разрешает парсинг в robots.txt
    2. Вы получили письменное разрешение
    3. Данные публичны и не защищены авторскими правами
    """
    # Проверяем robots.txt
    parsed = requests.utils.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    try:
        robots = requests.get(robots_url, headers=HEADERS, timeout=5)
        if "Disallow: /" in robots.text:
            print("❌ Сайт запрещает парсинг в robots.txt")
            return None
    except:
        pass
    
    time.sleep(1)  # Разумная задержка
    
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Парсим ТОЛЬКО заголовки и метаданные
    title = soup.find("title")
    return {
        "title": title.text if title else "No title",
        "url": url
    }
```

#### Рекомендация
**Используйте RSS-фиды вместо парсинга.** RSS специально создан для агрегации и является легальным способом получения новостей.

---

## Итоговая рекомендация для Telegram-бота

### 🏆 Топ-3 лучших решения для утренней сводки на русском языке

#### 1 место: RSS-фиды российских СМИ ⭐⭐⭐⭐⭐
**Рекомендуется как основной источник**

```python
# Оптимальная конфигурация для Telegram-бота
RSS_FEEDS_PRIMARY = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
    "Коммерсант": "https://www.kommersant.ru/RSS/news.xml",
    "Ведомости": "https://www.vedomosti.ru/rss/news",
}
```

**Почему RSS -- лучший выбор:**
- Полный контент на русском языке
- Без ограничений и API-ключей
- Реальное время
- Легально (RSS создан для агрегации)
- Надежно (работает десятилетиями)
- Низкая нагрузка (легкие XML-файлы)

#### 2 место: Currents API ⭐⭐⭐⭐⭐
**Рекомендуется как дополнительный/резервный источник**

- Лучший бесплатный тариф (1,000 запросов/день)
- Реальное время
- 120,000+ источников
- Коммерческое использование разрешено
- Поддержка русского языка

#### 3 место: Google News RSS ⭐⭐⭐⭐☆
**Рекомендуется для поиска по темам**

- Без ограничений
- Агрегация множества источников
- Поиск по ключевым словам
- Не требует API-ключа

---

### Рекомендуемая архитектура бота

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram Bot (Python)                     │
│                     aiogram/python-telegram-bot               │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Scheduler  │  │  News Engine │  │  Message Builder │   │
│  │  (APScheduler│  │              │  │                  │   │
│  │   или cron) │  │              │  │                  │   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘   │
│         │                │                     │             │
│    8:00 MSK      ┌───────┴───────┐      Format HTML        │
│    (ежедневно)   │               │      Truncate 4000     │
│         │   ┌────┴────┐   ┌─────┴─────┐     chars         │
│         │   │ RSS     │   │ Currents  │                   │
│         └──►│ Primary │   │ Backup    │◄──────────────────┘
│             │ Feed    │   │ API       │
│             │ Parser  │   │           │
│             └────┬────┘   └─────┬─────┘
│                  │              │
│             ┌────┴────┐    ┌────┴────┐
│             │ РИА     │    │ NewsData│
│             │ ТАСС    │    │ (opt)   │
│             │ Лента   │    └─────────┘
│             │ РБК     │
│             │ Коммерс │
│             │ Ведом   │
│             └─────────┘
│
│  ┌─────────────────────────────────────────────┐
│  │           Cache Layer (опционально)          │
│  │     SQLite/Redis для дедупликации            │
│  │     и хранения истории                       │
│  └─────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

---

### Пример полной реализации бота

```python
#!/usr/bin/env python3
"""
Telegram News Bot -- Утренняя сводка новостей
Использует RSS-фиды как основной источник
"""

import asyncio
import logging
import feedparser
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re
import html

# ─── Configuration ─────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "@your_channel"  # или ID чата

RSS_SOURCES = {
    "РИА Новости": "https://ria.ru/export/rss2/index.xml",
    "ТАСС": "https://tass.ru/rss/v2.xml",
    "Лента.ру": "https://lenta.ru/rss/news",
    "РБК": "https://rssexport.rbc.ru/rbcnews/news/30/rsslite.rss",
    "Коммерсант": "https://www.kommersant.ru/RSS/news.xml",
    "Ведомости": "https://www.vedomosti.ru/rss/news",
}

MAX_NEWS_PER_SOURCE = 3
MAX_TOTAL_NEWS = 15

# ─── Setup ──────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# ─── Functions ──────────────────────────────────────────────────────
def clean_html(text):
    """Очистка HTML-тегов"""
    clean = re.sub(r'<[^>]+>', '', text or "")
    return html.unescape(clean)

def truncate_text(text, max_length=200):
    """Обрезка текста до указанной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

async def fetch_rss_news():
    """Получение новостей из RSS-фидов"""
    all_news = []
    
    for source_name, feed_url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:MAX_NEWS_PER_SOURCE]:
                news_item = {
                    'title': clean_html(entry.get('title', '')),
                    'link': entry.get('link', ''),
                    'summary': truncate_text(clean_html(entry.get('summary', ''))),
                    'source': source_name,
                    'published': entry.get('published', '')
                }
                all_news.append(news_item)
        except Exception as e:
            logging.error(f"Error fetching {source_name}: {e}")
    
    return all_news[:MAX_TOTAL_NEWS]

def format_digest(news_items):
    """Форматирование сводки новостей"""
    today = datetime.now().strftime("%d.%m.%Y")
    
    digest = f"🌅 <b>Утренняя сводка новостей</b>\n"
    digest += f"📅 {today}\n"
    digest += "━" * 20 + "\n\n"
    
    current_source = None
    for item in news_items:
        if item['source'] != current_source:
            current_source = item['source']
            digest += f"📍 <b>{current_source}</b>\n"
        
        title = html.escape(item['title'])
        digest += f"  • <a href='{item['link']}'>{title}</a>\n"
    
    digest += f"\n━" * 20 + "\n"
    digest += f"📊 Всего новостей: {len(news_items)}\n"
    digest += "<i>Источники: РИА, ТАСС, Лента, РБК, Коммерсант, Ведомости</i>"
    
    return digest

async def send_morning_digest():
    """Отправка утренней сводки"""
    try:
        news = await fetch_rss_news()
        if news:
            digest = format_digest(news)
            await bot.send_message(
                chat_id=CHAT_ID,
                text=digest,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            logging.info(f"Morning digest sent: {len(news)} news items")
    except Exception as e:
        logging.error(f"Error sending digest: {e}")

# ─── Handlers ───────────────────────────────────────────────────────
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот новостей.\n\n"
        "📰 Каждое утро в 8:00 я присылаю сводку главных новостей.\n\n"
        "Команды:\n"
        "/digest -- Получить сводку сейчас\n"
        "/help -- Помощь"
    )

@dp.message(Command("digest"))
async def cmd_digest(message: types.Message):
    await message.answer("⏳ Собираю новости...")
    await send_morning_digest()

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📰 <b>Бот утренней сводки</b>\n\n"
        "Источники:\n"
        "• РИА Новости\n"
        "• ТАСС\n"
        "• Лента.ру\n"
        "• РБК\n"
        "• Коммерсант\n"
        "• Ведомости\n\n"
        "Команды:\n"
        "/digest -- Получить сводку\n"
        "/help -- Эта помощь",
        parse_mode="HTML"
    )

# ─── Scheduler ──────────────────────────────────────────────────────
async def on_startup():
    """Запуск планировщика"""
    scheduler.add_job(
        send_morning_digest,
        'cron',
        hour=8,
        minute=0,
        timezone='Europe/Moscow'
    )
    scheduler.start()
    logging.info("Bot started. Morning digest scheduled for 8:00 MSK")

# ─── Main ───────────────────────────────────────────────────────────
async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Требования к окружению

```bash
# Установка зависимостей
pip install aiogram apscheduler feedparser requests beautifulsoup4

# Или через requirements.txt:
# aiogram>=3.0
# apscheduler>=3.10
# feedparser>=6.0
# requests>=2.28
# beautifulsoup4>=4.11
```

---

### requirements.txt

```
aiogram>=3.0
apscheduler>=3.10
feedparser>=6.0
requests>=2.28
beautifulsoup4>=4.11
```

---

## Сравнительная таблица для Telegram-бота (утренняя сводка)

| Критерий | RSS-фиды | Currents API | GNews | NewsData.io | NewsAPI |
|----------|----------|-------------|-------|-------------|---------|
| **Русский язык** | ✅ Полный | ✅ Да | ✅ Да | ✅ Да | ✅ Да |
| **Реальное время** | ✅ Да | ✅ Да | ✅ Да | ⚠️ 12ч | ❌ 24ч |
| **Без API-ключа** | ✅ Да | ❌ Нет | ❌ Нет | ❌ Нет | ❌ Нет |
| **Без лимитов** | ✅ Да | ⚠️ 1000/д | ⚠️ 100/д | ⚠️ 200/д | ⚠️ 100/д |
| **Простота** | ✅ Высокая | ✅ Высокая | ✅ Высокая | ✅ Средняя | ✅ Высокая |
| **Надежность** | ✅ Высокая | ✅ Высокая | ✅ Высокая | ✅ Высокая | ✅ Высокая |
| **Качество контента** | ✅ Оригинал | ⚠️ Сниппет | ⚠️ Сниппет | ⚠️ Сниппет | ⚠️ Сниппет |
| **Легальность** | ✅ RSS для этого | ✅ Да | ✅ Да | ✅ Да | ❌ Dev only |
| **Цена** | ✅ Free | ✅ Free | ✅ Free | ✅ Free | ✅ Free |
| **Итоговый рейтинг** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐★☆ | ⭐⭐⭐★☆ | ⭐⭐☆☆☆ |

---

## Заключение

Для Telegram-бота с утренней сводкой новостей на русском языке **оптимальным решением** является комбинация:

1. **RSS-фиды** (основной источник) -- бесплатно, без лимитов, полный контент на русском
2. **Currents API** (резервный/дополнительный) -- на случай проблем с RSS
3. **Google News RSS** (поиск по темам) -- для специализированных запросов

Такая комбинация обеспечит надежную, бесплатную и легальную доставку новостей вашим пользователям.

---

*Исследование проведено в июле 2026 года. Информация актуальна на момент написания, но API-сервисы могут изменять условия. Всегда проверяйте актуальные тарифы на официальных сайтах.*
