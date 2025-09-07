# Docker развертывание Django проекта forchan

## 🐳 Обзор

Проект настроен для развертывания с использованием Docker контейнеров и поддерживает три различных сервера приложений:

- **uWSGI** - высокопроизводительный WSGI сервер
- **Gunicorn** - популярный WSGI сервер 
- **Uvicorn** - современный ASGI сервер с поддержкой WebSocket

## 📁 Структура Docker файлов

```
├── Dockerfile              # Основной Dockerfile (Uvicorn)
├── Dockerfile.uwsgi        # Dockerfile для uWSGI
├── Dockerfile.gunicorn     # Dockerfile для Gunicorn  
├── Dockerfile.uvicorn      # Dockerfile для Uvicorn
├── docker-compose.yml      # Основной compose файл
├── docker-run.sh          # Скрипт для удобного запуска
├── nginx.conf             # Конфигурация Nginx
└── .dockerignore          # Исключения для Docker
```

## 🚀 Быстрый запуск

### Простой запуск (рекомендуется)
```bash
# Запуск с Uvicorn (лучше для WebSocket)
./docker-run.sh uvicorn

# Запуск с Gunicorn
./docker-run.sh gunicorn

# Запуск с uWSGI
./docker-run.sh uwsgi
```

### С дополнительными сервисами
```bash
# С Nginx reverse proxy
./docker-run.sh uvicorn --with-nginx

# С PostgreSQL вместо SQLite
./docker-run.sh uvicorn --with-postgres

# Полная конфигурация
./docker-run.sh uvicorn --with-nginx --with-postgres
```

## 🛠 Управление контейнерами

### Остановка
```bash
./docker-run.sh --down
```

### Просмотр логов
```bash
./docker-run.sh --logs
# или для конкретного сервера
./docker-run.sh uvicorn --logs
```

### Пересборка образов
```bash
./docker-run.sh uvicorn --build
```

## 🔧 Ручное управление через docker-compose

### Запуск с конкретным сервером
```bash
# Uvicorn (рекомендуется для WebSocket)
docker-compose --profile uvicorn up -d

# Gunicorn
docker-compose --profile gunicorn up -d

# uWSGI
docker-compose --profile uwsgi up -d
```

### С дополнительными сервисами
```bash
# С PostgreSQL
docker-compose --profile uvicorn --profile postgres up -d

# С Nginx
docker-compose --profile uvicorn --profile nginx up -d

# Полная конфигурация
docker-compose --profile uvicorn --profile postgres --profile nginx up -d
```

### Выполнение Django команд
```bash
# Миграции
docker-compose --profile uvicorn run --rm app-uvicorn python manage.py migrate

# Создание суперпользователя
docker-compose --profile uvicorn run --rm app-uvicorn python manage.py createsuperuser

# Сбор статических файлов
docker-compose --profile uvicorn run --rm app-uvicorn python manage.py collectstatic
```

## 🌐 Доступные URL

### Без Nginx
- **Веб-сайт**: http://localhost:8000
- **Админка**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### С Nginx
- **Веб-сайт**: http://localhost
- **Админка**: http://localhost/admin/
- **API**: http://localhost/api/

## 📊 Сравнение серверов для Docker

| Сервер   | WebSocket | Размер образа | Время старта | Рекомендация |
|----------|-----------|---------------|--------------|--------------|
| Uvicorn  | ✅        | ~200MB        | Быстрый      | ⭐⭐⭐⭐⭐     |
| Gunicorn | ❌        | ~190MB        | Быстрый      | ⭐⭐⭐⭐      |
| uWSGI    | ❌        | ~195MB        | Средний      | ⭐⭐⭐        |

## 🔍 Мониторинг и логи

### Просмотр логов контейнеров
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app-uvicorn
docker-compose logs -f redis
docker-compose logs -f nginx
```

### Мониторинг ресурсов
```bash
# Использование ресурсов
docker stats

# Информация о контейнерах
docker-compose ps
```

## 🗄 База данных

### SQLite (по умолчанию)
- Файл базы данных хранится в контейнере
- Подходит для разработки и небольших проектов
- Автоматически создается при первом запуске

### PostgreSQL (опционально)
```bash
# Запуск с PostgreSQL
./docker-run.sh uvicorn --with-postgres
```

Настройки подключения:
- **База данных**: forchan
- **Пользователь**: forchan_user
- **Пароль**: forchan_password
- **Хост**: db
- **Порт**: 5432

## 📦 Volumes (тома)

Проект использует следующие тома Docker:

- `redis_data` - данные Redis
- `postgres_data` - данные PostgreSQL (если используется)
- `static_volume` - статические файлы Django
- `./media` - загруженные медиа файлы (bind mount)

## 🔒 Безопасность

### В контейнерах
- Приложение запускается под непривилегированным пользователем `app`
- Используются многоэтапные сборки для минимизации размера образов
- Системные пакеты очищаются после установки

### Рекомендации для production
1. Используйте переменные окружения для секретных данных
2. Настройте HTTPS через Nginx
3. Используйте внешнюю базу данных
4. Настройте мониторинг и алерты
5. Регулярно обновляйте базовые образы

## 🚨 Решение проблем

### Порты заняты
```bash
# Проверка занятых портов
netstat -tulpn | grep :8000
# или
lsof -i :8000

# Остановка всех контейнеров
docker-compose down
```

### Проблемы с правами доступа
```bash
# Очистка volumes
docker-compose down -v

# Пересборка образов
docker-compose build --no-cache
```

### Проблемы с базой данных
```bash
# Сброс базы данных (осторожно!)
docker-compose down -v
docker-compose --profile uvicorn up -d
```

### Проблемы с Redis
```bash
# Перезапуск Redis
docker-compose restart redis

# Проверка логов Redis
docker-compose logs redis
```

## 🔄 Обновление проекта

```bash
# 1. Остановка контейнеров
./docker-run.sh --down

# 2. Обновление кода (git pull, etc.)
git pull origin main

# 3. Пересборка и запуск
./docker-run.sh uvicorn --build
```

## 📝 Переменные окружения

Основные переменные окружения в контейнерах:

```env
DJANGO_SETTINGS_MODULE=forchan.settings
DJANGO_DEBUG=False
```

Для кастомизации создайте файл `.env`:

```env
# .env файл
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost
DATABASE_URL=postgresql://user:pass@db:5432/dbname
REDIS_URL=redis://redis:6379/0
```

## 🎯 Рекомендации

### Для разработки
- Используйте `uvicorn` профиль для поддержки WebSocket
- Оставьте SQLite для простоты
- Не используйте Nginx

### Для production
- Используйте `uvicorn` с `nginx` и `postgres` профилями
- Настройте домен и SSL сертификаты
- Используйте внешний Redis для масштабируемости
- Настройте резервное копирование базы данных

### Команда для production
```bash
./docker-run.sh uvicorn --with-nginx --with-postgres --build
```
