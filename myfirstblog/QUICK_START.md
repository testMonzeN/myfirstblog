# Быстрый старт - Docker развертывание

## 🐳 Запуск с Docker (рекомендуется)

### Простой запуск
```bash
# Uvicorn (лучший для WebSocket)
./docker-run.sh uvicorn

# Gunicorn (популярный выбор)
./docker-run.sh gunicorn

# uWSGI (максимальная производительность)
./docker-run.sh uwsgi
```

### Полное развертывание
```bash
# С Nginx и PostgreSQL
./docker-run.sh uvicorn --with-nginx --with-postgres
```

## 📋 Управление

```bash
# Остановка
./docker-run.sh --down

# Просмотр логов
./docker-run.sh --logs

# Пересборка
./docker-run.sh uvicorn --build
```

## 🌐 Доступные URL

- **Веб-сайт**: http://localhost:8000 (или http://localhost с nginx)
- **Админка**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

## 🔧 Альтернативный запуск (без Docker)

### Стандартный Django сервер разработки
```bash
python manage.py runserver
```

### Установка серверов вручную
```bash
# Установка зависимостей
pip install -r requirements.txt

# Миграции
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск с Uvicorn
uvicorn forchan.asgi:application --host 127.0.0.1 --port 8000 --reload
```

## ✨ Особенности проекта

- ✅ **WebSocket (channels)** - поддерживается в Docker
- ✅ **Django REST API** - работает со всеми серверами
- ✅ **Redis** - автоматически запускается в Docker
- ✅ **Статические файлы** - автоматически собираются
- ✅ **Media файлы** - сохраняются в volume

## 🎯 Рекомендации

### Для разработки
```bash
./docker-run.sh uvicorn
```

### Для production
```bash
./docker-run.sh uvicorn --with-nginx --with-postgres --build
```

## 📚 Подробная документация

- `DOCKER_DEPLOYMENT.md` - полное руководство по Docker
- `DEPLOYMENT_GUIDE.md` - классическое развертывание (устарело)
