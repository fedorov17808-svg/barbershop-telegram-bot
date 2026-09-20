# 🤖 Telegram Bot для Барбершопа - Практический Гайд

Полное руководство по внедрению Telegram бота для записи на услуги в барбершопе.

---

## 📋 Оглавление

1. [Рекомендуемое Решение](#рекомендуемое-решение)
2. [Архитектура Системы](#архитектура-системы)
3. [Функционал](#функционал)
4. [Примеры Интеграции](#примеры-интеграции)
5. [Альтернативы](#альтернативы)
6. [Развертывание](#развертывание)

---

## ✅ Рекомендуемое Решение

### Xaveron/barbershop-bot

**GitHub Repository:** https://github.com/Xaveron/barbershop-bot  
**Язык:** Python  
**Framework:** Aiogram 3  
**Лицензия:** MIT (Open Source)  
**Статус:** Активно разрабатывается

### Почему Именно Этот Бот?

✅ **SaaS архитектура** - один бот обслуживает несколько барбершопов  
✅ **Полная функциональность** - для клиентов и администраторов  
✅ **Защита от конфликтов** - тройная защита от двойной записи  
✅ **PostgreSQL + Redis** - профессиональный стек  
✅ **Docker** - легко развертывается  
✅ **Многоязычность** - RU, RO, EN  
✅ **Open Source** - можно кастомизировать  

---

## 🏗️ Архитектура Системы

### Компоненты

```
┌─────────────────────────────────────────────────────┐
│                    Telegram Clients                 │
│              (Users & Admin Chat IDs)               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│            Aiogram 3 Bot (Python 3.12)              │
│  - Webhook/Long Polling server                      │
│  - Message routing                                  │
│  - State management (FSM)                           │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌──────┐      ┌──────┐      ┌──────┐
    │ User │      │ Admin │    │Cache │
    │ Logic│      │ Logic │    │Redis │
    └──────┘      └──────┘     └──────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │PostgreSQL  │APScheduler│ │Database  │
   │Database│  │(Reminders)│  │Backups   │
   └─────────┘  └──────────┘  └──────────┘
```

### Технологический Стек

| Компонент | Версия | Назначение |
|-----------|--------|-----------|
| Python | 3.12 | Язык программирования |
| Aiogram | 3.x | Framework для Telegram Bot API |
| PostgreSQL | 16 | Основная БД |
| SQLAlchemy | 2.x | ORM для Python |
| Alembic | 1.x | Миграции БД |
| Redis | Latest | Кеширование и сессии |
| APScheduler | 3.x | Планировщик задач (напоминания) |
| Docker | Latest | Контейнеризация |

---

## 🎯 Функционал

### Для Клиентов (User Bot)

#### Основные Команды

```
/start               - начать общение
/menu               - главное меню
/book               - записаться на услугу
/my_bookings        - мои записи
/cancel_booking     - отменить запись
/faq                - часто задаваемые вопросы
/help               - помощь
```

#### Процесс Записи

```
1. /book
   ↓
2. Выбор филиала (если несколько)
   ↓
3. Выбор услуги (стрижка, борода, комбо)
   ↓
4. Выбор мастера (или "любой")
   ↓
5. Выбор даты
   ↓
6. Выбор времени (показываются только свободные)
   ↓
7. Подтверждение
   ↓
8. Запись создана! ✅

Уведомления:
→ Сразу после записи (с деталями)
→ За 24 часа до визита
→ За 2 часа до визита
```

#### Просмотр Записей

```
/my_bookings

Вывод:
─────────────────────
Запись #1234
Услуга: Мужская стрижка
Мастер: Иван
Дата: 25 сентября
Время: 15:30
Статус: ✅ Подтверждена

[Отменить запись] [Перенести]
─────────────────────
```

#### FAQ в Боте

```
/faq

Показывает:
❓ Как записаться?
❓ Какие услуги?
❓ Какие цены?
❓ Можно ли отменить?
❓ Нужно ли мыть голову?
❓ Есть ли парковка?
❓ Скидки постоянным?

Каждый вопрос - кликабельная кнопка
```

### Для Администраторов (Admin Panel)

#### Admin Menu

```
/admin

Администратор видит:
┌─────────────────────────────────┐
│  1️⃣ Управление филиалами        │
│  2️⃣ Управление услугами         │
│  3️⃣ Управление мастерами        │
│  4️⃣ Управление расписанием      │
│  5️⃣ Аналитика                   │
│  6️⃣ Роли и привилегии           │
│  7️⃣ Экспорт данных              │
└─────────────────────────────────┘
```

#### Управление Филиалами

```
Добавить филиал:
- Название
- Адрес
- Часы работы
- Телефон
- Координаты (для карты)

Редактировать:
- Все поля выше
- Перенести всех клиентов при закрытии

Удалить:
- С архивированием данных
```

#### Управление Услугами

```
Добавить услугу:
- Название (Мужская стрижка, Борода, и т.д.)
- Описание
- Цена
- Продолжительность (в минутах)
- Какие мастера могут выполнять
- Фото услуги (опционально)

Примеры:
┌──────────────────┬────────┬──────────┐
│ Услуга           │ Цена   │ Время    │
├──────────────────┼────────┼──────────┤
│ Мужская стрижка  │ 1200р  │ 40 мин   │
│ Борода           │ 800р   │ 25 мин   │
│ Комбо            │ 1800р  │ 60 мин   │
│ Кол. бритье      │ 1500р  │ 45 мин   │
└──────────────────┴────────┴──────────┘
```

#### Управление Мастерами

```
Добавить мастера:
- Имя
- Фото
- Описание/специализация
- Какие услуги выполняет
- Уровень квалификации
- Дата начала работы

Редактировать расписание:
- Выходные дни
- Часы работы каждого дня
- Отпуск
- Перерывы

Статистика по мастерам:
- Количество клиентов в месяц
- Средний рейтинг
- Доход
- No-show rate
```

#### Аналитика (Premium)

```
Доступные метрики:
📊 Количество записей за период
💰 Доход по услугам
👥 Новые клиенты vs повторные
⏱️ Среднее время между визитами
🚫 No-show rate (не пришли)
⭐ Средняя оценка (если есть)
📅 Пиковые дни и часы

CSV-экспорт:
- Все записи за период
- Клиенты с контактами
- Доход по мастерам
```

---

## 💡 Примеры Интеграции

### Пример 1: Простая Интеграция

Если вам нужен бот только для записи:

```python
# minimal_bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="📋 Мои записи")],
            [KeyboardButton(text="❓ FAQ")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать в [НАЗВАНИЕ] барбершопа!",
        reply_markup=kb
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
```

### Пример 2: С Базой Данных

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # Telegram User ID
    master_id = Column(Integer)
    service_id = Column(Integer)
    booking_date = Column(DateTime)
    created_at = Column(DateTime)
    status = Column(String)  # confirmed, cancelled, completed
    
class Master(Base):
    __tablename__ = "masters"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(Integer, nullable=True)
    services = Column(String)  # JSON
    schedule = Column(String)  # JSON
```

### Пример 3: Уведомления и Напоминания

```python
# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()

async def send_reminders():
    """Отправляет напоминания за 2 часа до записи"""
    from_time = datetime.now()
    to_time = from_time + timedelta(hours=2, minutes=30)
    
    bookings = db.query(Booking).filter(
        Booking.booking_date.between(from_time, to_time),
        Booking.status == "confirmed"
    ).all()
    
    for booking in bookings:
        message = f"""
📅 Напоминание о записи!

Услуга: {booking.service.name}
Мастер: {booking.master.name}
Время: {booking.booking_date.strftime("%H:%M")}

⏰ Осталось менее 2 часов!

[Отменить запись] [Перенести]
        """
        await bot.send_message(booking.user_id, message)

# Запускать каждый час
scheduler.add_job(send_reminders, 'interval', hours=1)
scheduler.start()
```

---

## 🔄 Альтернативы

### Если Хочешь Готовое Решение (No Code)

#### 1. **BotHelp** 
- URL: https://bothelp.io/ru/templates/zapis-v-salon-krasoty
- Преимущества: Визуальный конструктор, не нужен код
- Недостатки: Ограниченная кастомизация, платная
- Цена: $20-100/месяц

#### 2. **Booksy**
- URL: https://booksy.com/
- Преимущества: Популярный, много интеграций
- Недостатки: Комиссия за записи (10-15%)
- Цена: Платная за записи

#### 3. **Setmore**
- URL: https://www.setmore.com/
- Преимущества: Простой интерфейс
- Недостатки: Есть лимиты на бесплатном плане
- Цена: Бесплатно + платные расширения

### Если Хочешь Кастомный Бот (Python)

#### 1. **Xaveron/barbershop-bot** ⭐ РЕКОМЕНДУЕМ
- GitHub: https://github.com/Xaveron/barbershop-bot
- Сложность: Средняя
- Цена: Бесплатно (Open Source)

#### 2. **py-ilya-dev/barbershop-telegram-bot**
- GitHub: https://github.com/py-ilya-dev/barbershop-telegram-bot
- Сложность: Низкая
- Цена: Бесплатно

#### 3. **GrDanyl/barbershop-tg-bot** (TypeScript)
- GitHub: https://github.com/GrDanyl/barbershop-tg-bot
- Сложность: Средняя
- Цена: Бесплатно

---

## 🚀 Развертывание

### Шаг 1: Создать Telegram Bot

```bash
# 1. Напиши в @BotFather
/newbot

# 2. Ответь на вопросы:
# Как будет зваться бот? → MyBarberBot
# Какой юзернейм? → my_barber_booking_bot

# 3. Получишь TOKEN:
# 5123456789:ABCDefGhIJklMNOPQRstUvwxyz

# 4. Сохрани этот токен в безопасности!
```

### Шаг 2: Установить Зависимости

```bash
# Клонируем репозиторий
git clone https://github.com/Xaveron/barbershop-bot.git
cd barbershop-bot

# Создаём виртуальное окружение
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### Шаг 3: Настроить БД

```bash
# Создаём файл .env
cat > .env << EOF
BOT_TOKEN=5123456789:ABCDefGhIJklMNOPQRstUvwxyz
DATABASE_URL=postgresql://user:password@localhost/barbershop_bot
REDIS_URL=redis://localhost:6379/0
EOF

# Создаём базу данных
createdb barbershop_bot

# Запускаем миграции
alembic upgrade head
```

### Шаг 4: Запустить Бота

```bash
# Development (Local Polling)
python main.py

# Production (Docker)
docker build -t barbershop-bot .
docker run --env-file .env barbershop-bot
```

### Шаг 5: Проверить Работу

```bash
# Откроешь Telegram и напишешь боту:
/start

# Должно появиться меню с опциями записи
```

---

## 📊 Метрики Успеха

### Что Отслеживать

| Метрика | Целевое значение | Как мерить |
|---------|------------------|-----------|
| Booking Success Rate | > 90% | Записи через бота / попытки |
| Avg Session Time | > 2 мин | Analytics |
| Reminder Open Rate | > 60% | Просмотры напоминаний |
| No-show Rate | < 15% | Не пришли / подтверждено |
| Bot Engagement | > 40% | Активные пользователи / месяц |

---

## ⚠️ Важно Помнить

1. **Безопасность**: Никогда не коммитай токен в git
2. **GDPR**: Если в ЕС - соответствуй требованиям GDPR
3. **Резервные копии**: Регулярно бекапь базу данных
4. **Мониторинг**: Отслеживай ошибки в логах
5. **Обновления**: Обновляй Aiogram и зависимости

---

**Дополнительные ресурсы:**
- Docs Aiogram: https://docs.aiogram.dev/
- PostgreSQL: https://www.postgresql.org/
- Docker: https://www.docker.com/

