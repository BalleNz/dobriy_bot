# Dobriy Bot — бот для мессенджера Max

Бот для мессенджера **Max**, написанный с использованием асинхронного фреймворка и DI-контейнера Dishka.  
Поддерживает FSM (конечный автомат состояний), обработку колбэков, интеграцию с PostgreSQL и запуск через Docker Compose.

## Технологии

- Python 3.11+
- aiohttp + httpx
- SQLAlchemy 2.0 + asyncpg (через psycopg2-binary в sync-режиме)
- Dishka (DI-контейнер)
- Docker + Docker Compose
- Max API

## Структура проекта

```
.
├── docker-compose.yml      # запуск PostgreSQL + бота
├── Dockerfile              # (должен быть в корне, см. ниже)
├── main.py                 # точка входа
├── source/                 # весь исходный код
├── requirements.txt        # зависимости
└── .env                    # переменные окружения (создаётся вручную)
```

## Самый простой способ запуска — через Docker (рекомендуется)

Эта инструкция подходит даже если у вас **никогда не было Docker**.  
Всё делается в несколько кликов и команд.

### Шаг 1. Установите Docker Desktop (один раз)

1. Перейдите на официальный сайт: https://www.docker.com/products/docker-desktop/
2. Нажмите большую синюю кнопку **Download for Windows** или **Download for Mac**  
   (Если у вас Linux — ниже будет отдельная инструкция)
3. Запустите скачанный установщик и нажмите «Далее → Далее → Установить».
4. После установки Docker Desktop автоматически запустится (иконка кита в трее).
5. Готово! Docker установлен и работает.

> Если у вас Linux (Ubuntu/Debian/Mint и т.д.) — выполните в терминале:
> ```bash
> sudo apt update && sudo apt install -y docker.io docker-compose
> sudo usermod -aG docker $USER
> ```
> Потом перезайдите в систему или выполните `newgrp docker`.

### Шаг 2. Скачайте проект

1. Создайте папку, например `dobriy_bot`, и откройте терминал (PowerShell / CMD / Terminal) в этой папке.
2. Выполните:

```bash
git clone https://github.com/BalleNz/dobriy_bot.git .
```
или просто скачайте архив с проектом и распакуйте всё в эту папку.

### Шаг 3. Создайте файл .env

В той же папке создайте файл с именем **`.env`** (обязательно с точкой в начале).

Откройте его в Блокноте или любом редакторе и вставьте:

```env
# База данных
POSTGRES_DB=max_bot
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

ACCESS_TOKEN=f9LHodD0cOIOXPOaYi1ASsQWIi2yRznZmkF9BOQmQ4L7Pfv-PgT3rlWRzhqH7xeKlniTRwLr_1jqp-1z59G2
DB_URL=postgresql+asyncpg://user:pass@localhost/charity_bot
VK_DOBRO_BASE=https://dobro.mail.ru
API_BASE=https://platform-api.max.ru
```

Сохраните файл.

### Шаг 4. Запустите бота одной командой

В той же папке откройте терминал и выполните:

```bash
docker compose up --build
```

Первый раз будет долго (5–15 минут) — Docker скачивает образы Python и PostgreSQL, собирает бота.

Когда увидите строки вроде:

```
max_bot    | INFO:__main__:Handling in StartHandler for user_id=...
postgres   | LOG:  database system is ready to accept connections
```

— значит всё работает!

Бот уже онлайн и готов принимать сообщения в мессенджере Max.

### Как остановить и запустить снова

- Чтобы остановить: нажмите `Ctrl + C` в терминале  
  или выполните в другом окне:
  ```bash
  docker compose down
  ```

- Чтобы запустить снова в фоне (не будет занимать терминал):
  ```bash
  docker compose up -d
  ```

- Чтобы посмотреть логи бота в реальном времени:
  ```bash
  docker compose logs -f max_bot
  ```

## Вариант запуска локально без Docker

1. Создайте и заполните `.env` (те же переменные, что выше).

2. Создайте виртуальное окружение и установите зависимости:

```bash
python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

3. Запустите PostgreSQL локально (или используйте удалённый сервер), создайте базу и пользователя согласно `.env`.

4. Запустите бота:

```bash
python main.py
```

## Переменные окружения (.env)

| Переменная            | Описание                                    | Пример                              |
|-----------------------|---------------------------------------------|-------------------------------------|
| `POSTGRES_DB`         | Название базы данных                        | `max_bot`                            |
| `POSTGRES_USER`       | Пользователь БД                             | `admin`                       |
| `POSTGRES_PASSWORD`   | Пароль пользователя БД                      | `admin`                    |
| `MAX_BOT_TOKEN`       | Токен вашего бота от Max                    | `f9LHodD0cOIOXPOaYi1ASsQWIi2yRznZmkF9BOQmQ4L7Pfv-PgT3rlWRzhqH7xeKlniTRwLr_1jqp-1z59G2`    |

> Без `MAX_BOT_TOKEN` бот не сможет авторизоваться в API Max.