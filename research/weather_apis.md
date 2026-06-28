# Бесплатные API погоды -- Исследование 2025-2026

> **Дата исследования:** Июль 2025
> **Цель:** Сравнительный анализ бесплатных API прогноза погоды для интеграции в Telegram-бота
> **Акцент:** Работоспособность для РФ/СНГ, актуальные лимиты, примеры кода Python

---

## Сравнительная таблица

| # | API | Бесплатный лимит | Без ключа | Покрытие РФ | Прогноз дней | Рейтинг |
|---|-----|-------------------|-----------|-------------|--------------|---------|
| 1 | **Open-Meteo** | 10 000/день | Да | Да | 16 | ★★★★★ |
| 2 | **OpenWeatherMap** | 1 000/день | Нет | Да | 5 (3ч) / 16 | ★★★★☆ |
| 3 | **WeatherAPI.com** | 1 млн/мес (~33к/день) | Нет | Да | 14 | ★★★★☆ |
| 4 | **Yandex.Weather API** | 50/день (вечно) / 5 000/день (30 дн) | Нет | **Отличное** | 7 (test) | ★★★★☆ |
| 5 | **Weather.gov (NWS)** | Нет лимита | Да (User-Agent) | **Нет** (только США) | 7 | ★★★★☆ |
| 6 | **Visual Crossing** | 1 000/день | Нет | Да | 15 | ★★★★☆ |
| 7 | **Tomorrow.io** | 500/день | Нет | Да | 14 | ★★★★☆ |
| 8 | **PirateWeather** | 10 000/мес | Нет | Да | 7 | ★★★★☆ |
| 9 | **Meteoblue** | 10 млн кредитов/год | Нет | Да | 7 (час) / 14 (день) | ★★★☆☆ |
| 10 | **Weatherbit** | 50/день | Нет | Да | 16 | ★★★☆☆ |
| 11 | **Weatherstack** | 100/мес | Нет | Да | 14 (платно) | ★★☆☆☆ |
| 12 | **RainViewer** | Бесплатно (личное) | Да | Да | 2ч радар | ★★★☆☆ |
| 13 | **7Timer** | Без лимита | Да | Да | 7 | ★★★☆☆ |
| 14 | **HGBrasil** | 1 500/день | Нет | Нет (только Бразилия) | 10 | ★★☆☆☆ |
| 15 | **ColorfulClouds (Caiyun)** | Демо-токен | Нет | Да (Китай лучше) | 7 | ★★★☆☆ |

---

## Детальный обзор каждого API

---

### 1. Open-Meteo

**Сайт:** https://open-meteo.com
**Документация:** https://open-meteo.com/en/docs
**GitHub:** https://github.com/open-meteo/open-meteo

#### Лимиты бесплатного тарифа
- **10 000 вызовов в день** на бесплатном API
- Для некоммерческого использования -- без регистрации и API-ключа
- Коммерческий API: `customer-api.open-meteo.com` с `&apikey=`
- Один вызов = 1 HTTP-запрос (но >10 переменных или >2 недель = множественные вызовы)

#### Типы данных
- Текущая погода
- Прогноз на 16 дней (ежечасный)
- Исторические данные за 80+ лет (с 1940)
- Морской прогноз
- Качество воздуха
- Геокодинг
- Высота над уровнем моря
- Прогноз наводнений

#### Региональное покрытие
- **Глобальное** -- работает для любой точки Земли по координатам
- **РФ/СНГ:** Да, полностью

#### Формат ответа (JSON)
```json
{
  "latitude": 55.7558,
  "longitude": 37.6173,
  "hourly": {
    "time": ["2025-07-15T00:00", "2025-07-15T01:00"],
    "temperature_2m": [18.2, 17.5],
    "relative_humidity_2m": [65, 70],
    "precipitation": [0.0, 0.5],
    "weather_code": [1, 2],
    "wind_speed_10m": [12.5, 15.0]
  }
}
```

#### Пример кода Python
```python
import requests

def get_weather_open_meteo(lat=55.7558, lon=37.6173):
    """Open-Meteo API -- не требует API-ключа"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,precipitation,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 7
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_open_meteo()
current = data.get("current", {})
print(f"Температура: {current.get('temperature_2m')} C")
```

#### Плюсы
- Без ключа и регистрации для некоммерческого использования
- Огромный лимит (10K/день)
- Высокое разрешение моделей (от 1 км)
- Открытый исходный код (AGPLv3)
- Возможность self-host
- Очень быстрые ответы (<10 мс)
- 80+ лет исторических данных

#### Минусы
- Коммерческое использование требует подписки
- Исторические данные и ensemble требуют Professional плана
- Нет русскоязычных описаний погоды

---

### 2. OpenWeatherMap

**Сайт:** https://openweathermap.org
**Документация:** https://openweathermap.org/api
**Цены:** https://openweathermap.org/price

#### Лимиты бесплатного тарифа
- **1 000 000 вызовов в месяц** (~33 000/день)
- **60 вызовов в минуту**
- One Call 3.0: первые 1 000 вызовов в день бесплатно

#### Типы данных
- Текущая погода
- Прогноз 5 дней / 3 часа
- Прогноз 16 дней (ежедневный)
- Почасовой прогноз 4 дня
- Качество воздуха
- Геокодинг
- Погодные карты
- Предупреждения о погоде
- Исторические данные (ограниченно)

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да, полностью

#### Формат ответа (JSON)
```json
{
  "coord": {"lon": 37.6173, "lat": 55.7558},
  "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}],
  "main": {
    "temp": 25.5,
    "feels_like": 24.8,
    "temp_min": 22.1,
    "temp_max": 27.3,
    "pressure": 1015,
    "humidity": 45
  },
  "wind": {"speed": 3.5, "deg": 180},
  "clouds": {"all": 0},
  "dt": 1721001600,
  "sys": {"country": "RU", "sunrise": 1720980000, "sunset": 1721036400}
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "your_api_key")

def get_weather_openweathermap(city="Moscow"):
    """OpenWeatherMap API -- требует API-ключ (бесплатный)"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_openweathermap("Moscow")
main = data.get("main", {})
print(f"Температура: {main.get('temp')} C")
print(f"Ощущается как: {main.get('feels_like')} C")
print(f"Влажность: {main.get('humidity')}%")
```

#### Плюсы
- Огромное сообщество разработчиков
- Хорошая документация
- SDK для многих языков
- Погодные карты
- Предупреждения о погоде
- Русскоязычные описания

#### Минусы
- Требует API-ключ (регистрация)
- Почасовой прогноз только 4 дня на бесплатном тарифе
- Исторические данные ограничены
- Требуется указание авторства

---

### 3. WeatherAPI.com

**Сайт:** https://www.weatherapi.com
**Документация:** https://www.weatherapi.com/docs/

#### Лимиты бесплатного тарифа
- **1 000 000 вызовов в месяц** (~33 000/день)
- Прогноз на 3 дня на бесплатном тарифе

#### Типы данных
- Текущая погода (реальное время)
- Прогноз до 14 дней (3 дня -- бесплатно)
- Историческая погода (с 2010)
- Будущая погода (до 365 дней вперед)
- Морская погода
- Астрономия
- Качество воздуха
- Пыльца
- Solar irradiance
- Часовой пояс
- IP lookup

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да, полностью

#### Формат ответа (JSON)
```json
{
  "location": {
    "name": "Moscow",
    "country": "Russia",
    "lat": 55.76,
    "lon": 37.62
  },
  "current": {
    "temp_c": 22.0,
    "feelslike_c": 20.5,
    "humidity": 55,
    "wind_kph": 15.5,
    "condition": {"text": "Partly cloudy", "code": 1003}
  },
  "forecast": {
    "forecastday": [
      {
        "date": "2025-07-15",
        "day": {"maxtemp_c": 25.0, "mintemp_c": 15.0, "daily_chance_of_rain": 20}
      }
    ]
  }
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("WEATHERAPI_KEY", "your_api_key")

def get_weather_weatherapi(city="Moscow"):
    """WeatherAPI.com -- требует API-ключ (1M вызовов/мес бесплатно)"""
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": city,
        "days": 3,
        "aqi": "yes",
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_weatherapi("Moscow")
current = data.get("current", {})
print(f"Температура: {current.get('temp_c')} C")
print(f"Условия: {current['condition']['text']}")
```

#### Плюсы
- Огромный лимит (1M/мес)
- Очень богатые данные (пыльца, астрономия, качество воздуха)
- Поддержка русского языка (`lang=ru`)
- Морская погода
- Solar irradiance для солнечной энергетики

#### Минусы
- Прогноз только 3 дня на бесплатном тарифе
- Требует API-ключ
- Требуется указание авторства

---

### 4. Yandex.Weather API

**Сайт:** https://yandex.ru/pogoda
**Документация:** https://yandex.com/dev/weather/doc/en/
**Цены:** https://yandex.com/dev/weather/doc/en/concepts/pricing

#### Лимиты бесплатного тарифа
| Тариф | Стоимость | Лимит запросов | Прогноз |
|-------|-----------|----------------|---------|
| На вашем сайте | Бесплатно | **50/день** | Текущая + 2 периода |
| Test | Бесплатно 30 дней | **5 000/день** | 7 дней |
| Commercial | От 30 000 руб/мес | От 1.5M/мес | До 10 дней |

**Важно:** Для Home Assistant Yandex предоставляет **бесплатные ключи**: https://yandex.ru/pogoda/b2b/smarthome

#### Типы данных
- Текущая погода
- Прогноз на 7 дней (test) / 10 дней (commercial)
- Почасовой прогноз
- Осадки (дождь/снег)
- Давление, влажность, ветер
- Время восхода/заката

#### Региональное покрытие
- **Основной фокус:** Россия и СНГ
- Глобальное покрытие ограничено
- **РФ/СНГ:** Отличное -- лучшая точность для региона

#### Формат ответа (JSON)
```json
{
  "now": 1721001600,
  "now_dt": "2025-07-15T00:00:00+03:00",
  "info": {"lat": 55.7558, "lon": 37.6173, "url": "https://yandex.ru/pogoda/213"},
  "fact": {
    "temp": 22,
    "feels_like": 20,
    "condition": "partly-cloudy",
    "wind_speed": 4,
    "wind_dir": "nw",
    "pressure_mm": 745,
    "humidity": 55,
    "precipitation_type": 0,
    "precipitation_strength": 0
  },
  "forecasts": [
    {
      "date": "2025-07-15",
      "hours": [{"hour": "0", "temp": 18, "condition": "clear"}]
    }
  ]
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("YANDEX_WEATHER_API_KEY", "your_api_key")

def get_weather_yandex(lat=55.7558, lon=37.6173):
    """Yandex.Weather API -- лучший для РФ/СНГ"""
    url = "https://api.weather.yandex.ru/v2/informers"
    headers = {"X-Yandex-Weather-Key": API_KEY}
    params = {
        "lat": lat,
        "lon": lon,
        "lang": "ru_RU"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_yandex()
fact = data.get("fact", {})
print(f"Температура: {fact.get('temp')} C")
print(f"Ощущается как: {fact.get('feels_like')} C")
print(f"Влажность: {fact.get('humidity')}%")
print(f"Условия: {fact.get('condition')}")
```

#### Плюсы
- **Лучшая точность для России и СНГ**
- Русскоязычные данные и условия
- Данные Yandex -- самые точные для РФ
- Бесплатный ключ для Home Assistant
- Официальная поддержка от Яндекса

#### Минусы
- Только 50 запросов/день на постоянном бесплатном тарифе
- Платный тариф дорогой (от 30 000 руб/мес)
- Требует API-ключ
- Нужно соблюдать правила брендинга
- При превышении лимита -- 403 ошибка до следующего дня

---

### 5. Weather.gov (National Weather Service / NOAA)

**Сайт:** https://www.weather.gov
**Документация:** https://www.weather.gov/documentation/services-web-api
**API URL:** https://api.weather.gov

#### Лимиты бесплатного тарифа
- **Полностью бесплатно**, без API-ключа
- Требуется заголовок `User-Agent`
- Генерасные rate limits (для типичного использования не достигаются)
- При превышении -- retry через ~5 секунд

#### Типы данных
- Прогноз на 7 дней (12-часовые периоды)
- Почасовой прогноз на 7 дней
- Raw forecast grid data
- Оповещения о погоде
- Наблюдения со станций
- Геокодирование

#### Региональное покрытие
- **Только США** (включая территории)
- **РФ/СНГ:** Нет

#### Формат ответа (JSON)
```json
{
  "properties": {
    "periods": [
      {
        "number": 1,
        "name": "Tonight",
        "startTime": "2025-07-15T20:00:00-04:00",
        "endTime": "2025-07-16T06:00:00-04:00",
        "temperature": 22,
        "temperatureUnit": "F",
        "windSpeed": "5 mph",
        "forecast": "Mostly clear"
      }
    ]
  }
}
```

#### Пример кода Python
```python
import requests

def get_weather_nws(lat=38.8894, lon=-77.0352):
    """NWS/NOAA API -- только США, без ключа, нужен User-Agent"""
    headers = {
        "User-Agent": "(myweatherapp.com, contact@myweatherapp.com)"
    }
    # Шаг 1: Получить metadata для точки
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    resp = requests.get(points_url, headers=headers)
    points_data = resp.json()
    
    # Шаг 2: Получить прогноз
    forecast_url = points_data["properties"]["forecast"]
    forecast_resp = requests.get(forecast_url, headers=headers)
    return forecast_resp.json()

# Использование (только для координат в США!)
data = get_weather_nws(38.8894, -77.0352)
periods = data.get("properties", {}).get("periods", [])
for p in periods[:3]:
    print(f"{p['name']}: {p['temperature']}F, {p['forecast']}")
```

#### Плюсы
- Полностью бесплатно
- Без API-ключа
- Данные от NOAA -- очень точные для США
- Предупреждения о погоде
- 2.5km grid resolution

#### Минусы
- **Только США** -- не работает для РФ/СНГ
- Сложная двухэтапная структура запросов
- Документация сложная
- Нет SLA

---

### 6. Visual Crossing Weather API

**Сайт:** https://www.visualcrossing.com/weather-api
**Документация:** https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/

#### Лимиты бесплатного тарифа
- **1 000 записей в день** бесплатно
- Исторические + прогноз + текущая погода
- CSV и JSON форматы

#### Типы данных
- Текущая погода
- Прогноз до 15 дней
- Исторические данные 50+ лет
- Статистика климата
- UV индекс
- Solar radiation
- Астрономия

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Формат ответа (JSON)
```json
{
  "latitude": 55.7558,
  "longitude": 37.6173,
  "resolvedAddress": "Moscow, Russia",
  "days": [
    {
      "datetime": "2025-07-15",
      "tempmax": 25.0,
      "tempmin": 15.0,
      "temp": 20.0,
      "humidity": 55.5,
      "windspeed": 12.0,
      "conditions": "Partially cloudy"
    }
  ]
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("VISUAL_CROSSING_KEY", "your_api_key")

def get_weather_visualcrossing(location="Moscow,Russia"):
    """Visual Crossing -- 1000 записей/день бесплатно"""
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/"
        f"rest/services/timeline/{location}"
    )
    params = {
        "unitGroup": "metric",
        "key": API_KEY,
        "contentType": "json",
        "include": "current,days"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_visualcrossing("Moscow,Russia")
days = data.get("days", [])
print(f"Сегодня: {days[0]['tempmax']}C max / {days[0]['tempmin']}C min")
```

#### Плюсы
- Единый endpoint для истории, текущей и прогноза
- 50+ лет исторических данных
- CSV и JSON
- Хорош для data science
- Коммерческое использование с указанием авторства

#### Минусы
- Требует API-ключ
- Только 1000 записей/день (не вызовов -- записей!)
- Нет air quality на бесплатном тарифе

---

### 7. Tomorrow.io (ранее ClimaCell)

**Сайт:** https://www.tomorrow.io
**Документация:** https://docs.tomorrow.io/
**Поддержка:** https://support.tomorrow.io

#### Лимиты бесплатного тарифа
- **500 запросов в день**
- **25 запросов в час**
- **3 запроса в секунду**
- Сброс в 00:00 UTC

#### Типы данных
- 80+ слоев данных
- Температура, ветер, осадки, влажность
- Качество воздуха
- Пыльца
- Дорожные риски
- Fire index
- UV
- Предупреждения о погоде
- Weather maps tiles

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Формат ответа (JSON)
```json
{
  "data": {
    "timelines": [
      {
        "timestep": "1h",
        "startTime": "2025-07-15T00:00:00Z",
        "endTime": "2025-07-22T00:00:00Z",
        "intervals": [
          {
            "startTime": "2025-07-15T00:00:00Z",
            "values": {
              "temperature": 22.5,
              "humidity": 55,
              "windSpeed": 5.2,
              "precipitationProbability": 10
            }
          }
        ]
      }
    ]
  }
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("TOMORROW_IO_KEY", "your_api_key")

def get_weather_tomorrow(lat=55.7558, lon=37.6173):
    """Tomorrow.io -- 500 запросов/день бесплатно"""
    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "apikey": API_KEY,
        "location": f"{lat},{lon}",
        "fields": ["temperature", "humidity", "windSpeed", "precipitationProbability"],
        "timesteps": "1h",
        "startTime": "now",
        "endTime": "nowPlus7d"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_tomorrow()
intervals = data.get("data", {}).get("timelines", [{}])[0].get("intervals", [])
if intervals:
    first = intervals[0]["values"]
    print(f"Температура: {first['temperature']} C")
```

#### Плюсы
- 80+ параметров погоды
- Гиперлокальный прогноз (до уровня улицы)
- ML/AI модели
- 99.9% uptime SLA
- Weather maps tiles
- Отличная документация

#### Минусы
- Всего 500 запросов/день
- Только 25/час
- Требует API-ключ
- Коммерческое использование платное

---

### 8. PirateWeather

**Сайт:** https://pirateweather.net
**Документация:** https://pirateweather.net/en/latest/API/
**GitHub:** https://github.com/Pirate-Weather/pirateweather

#### Лимиты бесплатного тарифа
- **10 000 вызовов в месяц** бесплатно
- Полная совместимость с форматом Dark Sky API

#### Типы данных
- Текущая погода
- Минутный прогноз (1 час)
- Почасовой прогноз (7 дней)
- Ежедневный прогноз (7 дней)
- Оповещения о погоде
- Исторические данные

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Формат ответа (JSON)
```json
{
  "latitude": 55.7558,
  "longitude": 37.6173,
  "currently": {
    "temperature": 22.5,
    "apparentTemperature": 21.0,
    "humidity": 0.55,
    "windSpeed": 5.2,
    "precipProbability": 0.1,
    "summary": "Partly Cloudy"
  },
  "hourly": {
    "summary": "Partly cloudy for the hour.",
    "data": [{"time": 1721001600, "temperature": 22.5}]
  },
  "daily": {
    "data": [{"time": 1721001600, "temperatureHigh": 25.0, "temperatureLow": 15.0}]
  }
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("PIRATEWEATHER_KEY", "your_api_key")

def get_weather_pirate(lat=55.7558, lon=37.6173):
    """PirateWeather -- 10K/мес, совместим с Dark Sky"""
    url = f"https://api.pirateweather.net/forecast/{API_KEY}/{lat},{lon}"
    params = {"units": "si"}
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_pirate()
current = data.get("currently", {})
print(f"Температура: {current.get('temperature')} C")
print(f"Ощущается: {current.get('apparentTemperature')} C")
print(f"Вероятность осадков: {current.get('precipProbability', 0) * 100}%")
```

#### Плюсы
- Drop-in замена Dark Sky API
- Open source
- Возможность self-host
- Простой формат данных
- CORS поддержка

#### Минусы
- Требует API-ключ
- Относительно новый сервис
- 10K/мес может быть мало
- Нет гарантий SLA

---

### 9. Meteoblue

**Сайт:** https://www.meteoblue.com
**Документация:** https://docs.meteoblue.com/en/weather-apis/introduction/overview
**Free API:** https://business.meteoblue.com/products/weather-apis/free-weather-api

#### Лимиты бесплатного тарифа
- **Бесплатный тест на 1 год** с 10 000 000 кредитов
- Каждый вызов стоит определенное количество кредитов
- Простой прогноз: ~4000 кредитов
- Сложные пакеты: до 16000 кредитов
- Rate limit: 500 вызовов/мин

#### Типы данных
- Текущая погода
- Почасовой прогноз 7 дней
- Ежедневный прогноз 14 дней
- Температура, влажность, ветер
- Осадки, снег, облачность
- UV индекс
- Weather maps
- Изображения (метеограммы)

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да
- Особенно сильны в Европе

#### Формат ответа (JSON)
```json
{
  "metadata": {
    "name": "Basel",
    "latitude": 47.558,
    "longitude": 7.573
  },
  "data_1h": {
    "time": ["2025-07-15T00:00", "2025-07-15T01:00"],
    "temperature": [18.2, 17.5],
    "precipitation": [0.0, 0.5],
    "windspeed": [12.5, 15.0]
  },
  "data_day": {
    "time": ["2025-07-15"],
    "temperature_max": [25.0],
    "temperature_min": [15.0]
  }
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("METEOBLUE_KEY", "DEMOKEY")

def get_weather_meteoblue(lat=55.7558, lon=37.6173):
    """Meteoblue -- 10M кредитов/год бесплатно (на 1 год)"""
    url = "https://my.meteoblue.com/packages/basic-1h_basic-day"
    params = {
        "lat": lat,
        "lon": lon,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_meteoblue()
hourly = data.get("data_1h", {})
print(f"Температура сейчас: {hourly['temperature'][0]} C")
```

#### Плюсы
- Высокая точность (особенно в Европе)
- Принадлежит Windy.com
- Комбинирование множества моделей с ML
- Богатый набор визуализаций

#### Минусы
- Бесплатно только на 1 год
- Сложная система кредитов
- Rate limit 500/мин
- Требует API-ключ

---

### 10. Weatherbit

**Сайт:** https://www.weatherbit.io
**Документация:** https://www.weatherbit.io/api

#### Лимиты бесплатного тарифа
- **50 вызовов в день** (снижено с 500 в 2022!)
- Прогноз 7 дней

#### Типы данных
- Текущая погода
- Прогноз до 16 дней
- Исторические данные 30+ лет
- Качество воздуха
- UV индекс
- Молнии
- Soil temperature & moisture (уникально!)
- Weather alerts (30+ стран)

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Формат ответа (JSON)
```json
{
  "data": [
    {
      "temp": 22.0,
      "app_temp": 21.0,
      "rh": 55,
      "weather": {"description": "Clear sky", "code": 800},
      "wind_spd": 3.5,
      "wind_dir": 180,
      "precip": 0.0,
      "clouds": 0
    }
  ]
}
```

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("WEATHERBIT_KEY", "your_api_key")

def get_weather_weatherbit(city="Moscow"):
    """Weatherbit -- 50 вызовов/день (очень мало!)"""
    url = "https://api.weatherbit.io/v2.0/current"
    params = {
        "city": city,
        "key": API_KEY,
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_weatherbit("Moscow")
if data.get("data"):
    w = data["data"][0]
    print(f"Температура: {w['temp']} C")
    print(f"Влажность: {w['rh']}%")
```

#### Плюсы
- Soil temperature & moisture (уникальные данные)
- Качество воздуха включено
- 30+ лет исторических данных
- ML-корректированные прогнозы

#### Минусы
- **Только 50 вызовов/день** -- слишком мало для бота!
- Дорогие платные планы (от $40/мес)
- 95% uptime SLA (низкий)

---

### 11. Weatherstack

**Сайт:** https://weatherstack.com
**Документация:** https://weatherstack.com/documentation
**Цены:** https://weatherstack.com/pricing

#### Лимиты бесплатного тарифа
- **100 вызовов в месяц** (очень мало!)
- Только текущая погода
- Без HTTPS

#### Типы данных
- Текущая погода
- Прогноз (платно)
- Исторические данные (платно)
- Location search (платно)
- Marine data (платно)
- Astronomy (платно)

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Пример кода Python
```python
import requests
import os

API_KEY = os.getenv("WEATHERSTACK_KEY", "your_api_key")

def get_weather_weatherstack(city="Moscow"):
    """Weatherstack -- 100 вызовов/мес (очень ограниченно)"""
    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": API_KEY,
        "query": city
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_weatherstack("Moscow")
current = data.get("current", {})
print(f"Температура: {current.get('temperature')} C")
```

#### Плюсы
- Простой API
- Глобальное покрытие

#### Минусы
- Всего 100 вызовов/месяц
- Без HTTPS на бесплатном тарифе
- Прогноз и история платные
- Для Telegram-бота практически бесполезен

---

### 12. RainViewer

**Сайт:** https://www.rainviewer.com
**Документация:** https://www.rainviewer.com/api.html
**GitHub:** https://github.com/rainviewer/rainviewer-api-example

#### Лимиты бесплатного тарифа
- **Бесплатно для личного/образовательного использования**
- Без регистрации и API-ключа
- Max zoom: 7 (512px tiles)
- Только past radar data (без nowcast)

#### Типы данных
- Радарные карты осадков
- 1200+ радаров в 150+ странах
- Обновление каждые 5 минут
- 2 часа исторических данных
- PNG tiles

#### Региональное покрытие
- **150+ стран**
- **РФ/СНГ:** Да (там где есть радары)

#### Пример кода Python
```python
import requests

def get_rainviewer_data():
    """RainViewer -- радар осадков, без ключа"""
    url = "https://api.rainviewer.com/public/weather-maps.json"
    response = requests.get(url)
    data = response.json()
    return data

# Получить последний кадр радара
data = get_rainviewer_data()
past = data.get("radar", {}).get("past", [])
if past:
    latest = past[-1]
    # Формат tile: /v2/radar/{timestamp}/256/{z}/{x}/{y}/2/1_1.png
    tile_url = f"https://tilecache.rainviewer.com{latest['path']}"
    print(f"Последний кадр радара: {tile_url}")
```

#### Плюсы
- Полностью бесплатно
- Без ключа
- 1200+ радаров
- Обновление каждые 5 минут

#### Минусы
- Только радарные данные (температура, ветер -- нет)
- Без nowcast на бесплатном тарифе
- Только для личного использования
- **API будет закрыт в январе 2026!**

---

### 13. 7Timer!

**Сайт:** https://www.7timer.info
**Документация:** https://www.7timer.info/doc.php?lang=en

#### Лимиты бесплатного тарифа
- **Без лимита**
- **Без ключа**
- Без регистрации

#### Типы данных
- Численный прогноз погоды
- Температура, влажность, ветер
- Осадки, облачность
- Прогноз на 7 дней

#### Региональное покрытие
- **Глобальное**
- **РФ/СНГ:** Да

#### Формат ответа (JSON)
```json
{
  "product": "civillight",
  "init": "2025071500",
  "dataseries": [
    {
      "date": 20250715,
      "temp2m": {"max": 25, "min": 15},
      "weather": "cloudy",
      "wind10m_max": 3
    }
  ]
}
```

#### Пример кода Python
```python
import requests

def get_weather_7timer(lat=55.7558, lon=37.6173):
    """7Timer -- без ключа, без лимитов"""
    url = "https://www.7timer.info/bin/civillight.php"
    params = {
        "lon": lon,
        "lat": lat,
        "ac": 0,
        "unit": "metric",
        "output": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_7timer()
for day in data.get("dataseries", [])[:3]:
    print(f"Дата: {day['date']}, Max: {day['temp2m']['max']}C, Min: {day['temp2m']['min']}C")
```

#### Плюсы
- Полностью бесплатно
- Без ключа и регистрации
- Без лимитов
- Простой API

#### Минусы
- Ограниченные данные
- Нет текущей погоды
- Только ежедневный прогноз (без почасового)
- Данные не очень точные

---

### 14. HGBrasil

**Сайт:** https://console.hgbrasil.com
**Документация:** https://console.hgbrasil.com/documentation/weather

#### Лимиты бесплатного тарифа
- **1 500 запросов в день**
- Только Бразилия

#### Типы данных
- Текущая погода
- Прогноз до 10 дней
- Влажность, осадки, ветер
- Восход/закат
- Фазы луны

#### Региональное покрытие
- **Только Бразилия**
- **РФ/СНГ:** Нет

#### Пример кода Python
```python
import requests

def get_weather_hgbrasil(city_code="BRXX0201"):
    """HGBrasil -- только Бразилия, 1500/день"""
    url = "https://api.hgbrasil.com/weather"
    params = {
        "key": "your_key",
        "woeid": city_code
    }
    response = requests.get(url, params=params)
    return response.json()
```

#### Плюсы
- Хорош для Бразилии
- Бесплатно

#### Минусы
- Только Бразилия -- не подходит для РФ/СНГ

---

### 15. ColorfulClouds (Caiyun Weather)

**Сайт:** https://www.caiyunapp.com
**Документация:** https://open.caiyunapp.com/ColorfulClouds_Weather_API

#### Лимиты бесплатного тарифа
- Демо-токен для тестирования
- Полноценный API требует регистрации и ключа

#### Типы данных
- Реальное время
- Почасовой прогноз (72 часа)
- Ежедневный прогноз (7 дней)
- Минутный прогноз осадков
- Качество воздуха
- Weather alerts
- Historical (24 часа)

#### Региональное покрытие
- **Глобальное**
- **Китай:** Лучшее качество (минутный прогноз)
- **РФ/СНГ:** Да, но качество ниже чем для Китая

#### Пример кода Python
```python
import requests

def get_weather_caiyun(lat=55.7558, lon=37.6173):
    """ColorfulClouds (Caiyun) -- демо-токен"""
    token = "S45Fnpxcwyq0QT4b"  # Демо-токен, ограниченный!
    url = f"https://api.caiyunapp.com/v2.5/{token}/{lon},{lat}/weather.json"
    params = {"lang": "en_US", "unit": "metric"}
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Использование
data = get_weather_caiyun()
result = data.get("result", {})
realtime = result.get("realtime", {})
print(f"Температура: {realtime.get('temperature')} C")
print(f"Влажность: {realtime.get('humidity')}")
```

#### Плюсы
- Минутный прогноз осадков (уникально)
- Глобальное покрытие
- Высокая точность в Китае
- 99.94% availability

#### Минусы
- Демо-токен сильно ограничен
- Нужен API-ключ
- Минутный прогноз работает не везде
- Документация на китайском

---

## Итоговая рекомендация для Telegram-бота

### Рекомендуемая стратегия: Multi-API с fallback

Для Telegram-бота, работающего с пользователями из РФ/СНГ, рекомендуется использовать комбинацию API:

```python
import requests
import os

# Конфигурация API
WEATHER_APIS = {
    "open_meteo": {"priority": 1, "needs_key": False},
    "yandex": {"priority": 2, "needs_key": True, "key": os.getenv("YANDEX_KEY")},
    "openweather": {"priority": 3, "needs_key": True, "key": os.getenv("OWM_KEY")},
    "weatherapi": {"priority": 4, "needs_key": True, "key": os.getenv("WEATHERAPI_KEY")},
}

def get_weather_with_fallback(lat, lon):
    """Получить погоду с fallback между API"""
    # 1. Пробуем Open-Meteo (не нужен ключ)
    try:
        return get_weather_open_meteo(lat, lon)
    except Exception:
        pass
    
    # 2. Пробуем Yandex (лучший для РФ)
    try:
        return get_weather_yandex(lat, lon)
    except Exception:
        pass
    
    # 3. Пробуем OpenWeatherMap
    try:
        city = f"{lat},{lon}"
        return get_weather_openweathermap(city)
    except Exception:
        pass
    
    # 4. Последний fallback -- 7Timer (без ключа)
    return get_weather_7timer(lat, lon)
```

### Приоритеты выбора:

| Приоритет | API | Когда использовать |
|-----------|-----|-------------------|
| 1 | **Open-Meteo** | Основной API -- не нужен ключ, большие лимиты, глобальное покрытие |
| 2 | **Yandex.Weather** | Для пользователей из РФ -- максимальная точность |
| 3 | **OpenWeatherMap** | Запасной вариант -- большое сообщество, русский язык |
| 4 | **WeatherAPI.com** | Если нужны специфические данные (пыльца, астрономия) |
| 5 | **7Timer** | Последний fallback -- всегда доступен |

### Ключевые выводы:

1. **Open-Meteo** -- лучший выбор для старта: не нужен ключ, 10K/день, отличные данные, open-source
2. **Yandex.Weather** -- обязателен для бота с пользователями из России (самые точные данные)
3. **OpenWeatherMap** -- надежный классический вариант с огромным сообществом
4. **WeatherAPI.com** -- если нужен широкий функционал (1M/мес)
5. **RainViewer** -- будет закрыт в январе 2026, не использовать для новых проектов
6. **Weatherstack** и **Weatherbit** -- слишком маленькие лимиты для Telegram-бота
7. **Weather.gov** -- только для ботов с пользователями из США

### Сравнение лимитов для Telegram-бота (наглядно):

```
Open-Meteo:        ████████████████████████████████████████  10 000/день (без ключа!)
OpenWeatherMap:    ████████████████████████████████          1 000/день
WeatherAPI.com:    ████████████████████████████████████████  33 000/день
Visual Crossing:   ████████████████████████████████████████  1 000/день
Tomorrow.io:       ████████████                            500/день
PirateWeather:     ████████                                333/день (10K/мес)
Yandex (беспл.):   █                                         50/день
Weatherbit:        █                                         50/день
Weatherstack:      ▌                                         3/день (100/мес)
7Timer:            ∞                                         Без лимита (без ключа!)
```

---

*Исследование проведено в июле 2025 года. Данные актуальны на момент составления. Рекомендуется перепроверять лимиты на официальных сайтах API перед production-использованием.*
