#!/bin/bash

# Скрипт для запуска Django проекта с разными серверами через Docker

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}"
    echo "=============================================="
    echo "🐳 Docker Deployment для Django проекта forchan"
    echo "=============================================="
    echo -e "${NC}"
}

print_help() {
    echo "Использование: $0 [СЕРВЕР] [ОПЦИИ]"
    echo ""
    echo "Доступные серверы:"
    echo "  uwsgi     - Запуск с uWSGI сервером"
    echo "  gunicorn  - Запуск с Gunicorn сервером"
    echo "  uvicorn   - Запуск с Uvicorn сервером (рекомендуется для WebSocket)"
    echo ""
    echo "Опции:"
    echo "  --with-nginx    - Запуск с Nginx reverse proxy"
    echo "  --with-postgres - Использовать PostgreSQL вместо SQLite"
    echo "  --build         - Пересобрать образы"
    echo "  --down          - Остановить и удалить контейнеры"
    echo "  --logs          - Показать логи"
    echo "  --help, -h      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 uvicorn                    # Запуск с Uvicorn"
    echo "  $0 gunicorn --with-nginx      # Запуск с Gunicorn и Nginx"
    echo "  $0 uwsgi --with-postgres      # Запуск с uWSGI и PostgreSQL"
    echo "  $0 --down                     # Остановить все контейнеры"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker не установлен!${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose не установлен!${NC}"
        exit 1
    fi
}

run_migrations() {
    local server=$1
    echo -e "${YELLOW}📦 Выполнение миграций базы данных...${NC}"
    
    if [[ "$server" == "postgres" ]]; then
        docker-compose --profile postgres --profile $server run --rm app-$server python manage.py migrate
    else
        docker-compose --profile $server run --rm app-$server python manage.py migrate
    fi
}

create_superuser() {
    local server=$1
    echo -e "${YELLOW}👤 Создание суперпользователя...${NC}"
    echo "Нажмите Ctrl+C если не хотите создавать суперпользователя"
    sleep 3
    
    if [[ "$server" == "postgres" ]]; then
        docker-compose --profile postgres --profile $server run --rm app-$server python manage.py createsuperuser || true
    else
        docker-compose --profile $server run --rm app-$server python manage.py createsuperuser || true
    fi
}

main() {
    print_banner
    check_docker
    
    # Парсинг аргументов
    SERVER=""
    WITH_NGINX=false
    WITH_POSTGRES=false
    BUILD=false
    DOWN=false
    LOGS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            uwsgi|gunicorn|uvicorn)
                SERVER="$1"
                shift
                ;;
            --with-nginx)
                WITH_NGINX=true
                shift
                ;;
            --with-postgres)
                WITH_POSTGRES=true
                shift
                ;;
            --build)
                BUILD=true
                shift
                ;;
            --down)
                DOWN=true
                shift
                ;;
            --logs)
                LOGS=true
                shift
                ;;
            --help|-h)
                print_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Неизвестный параметр: $1${NC}"
                print_help
                exit 1
                ;;
        esac
    done
    
    # Остановка контейнеров
    if [[ "$DOWN" == true ]]; then
        echo -e "${YELLOW}🛑 Остановка всех контейнеров...${NC}"
        docker-compose down -v
        echo -e "${GREEN}✅ Контейнеры остановлены${NC}"
        exit 0
    fi
    
    # Показ логов
    if [[ "$LOGS" == true ]]; then
        if [[ -z "$SERVER" ]]; then
            docker-compose logs -f
        else
            docker-compose logs -f app-$SERVER
        fi
        exit 0
    fi
    
    # Проверка выбора сервера
    if [[ -z "$SERVER" ]]; then
        echo -e "${RED}❌ Необходимо указать сервер!${NC}"
        print_help
        exit 1
    fi
    
    # Формирование команды docker-compose
    COMPOSE_CMD="docker-compose"
    PROFILES="--profile $SERVER"
    
    if [[ "$WITH_POSTGRES" == true ]]; then
        PROFILES="$PROFILES --profile postgres"
        echo -e "${BLUE}🐘 Используется PostgreSQL${NC}"
    else
        echo -e "${BLUE}📄 Используется SQLite${NC}"
    fi
    
    if [[ "$WITH_NGINX" == true ]]; then
        PROFILES="$PROFILES --profile nginx"
        echo -e "${BLUE}🌐 Используется Nginx${NC}"
    fi
    
    # Сборка образов
    if [[ "$BUILD" == true ]]; then
        echo -e "${YELLOW}🔨 Сборка образов...${NC}"
        $COMPOSE_CMD $PROFILES build
    fi
    
    echo -e "${BLUE}🚀 Запуск с сервером: ${SERVER}${NC}"
    
    # Запуск контейнеров
    $COMPOSE_CMD $PROFILES up -d
    
    # Ожидание запуска
    echo -e "${YELLOW}⏳ Ожидание запуска контейнеров...${NC}"
    sleep 5
    
    # Выполнение миграций
    if [[ "$WITH_POSTGRES" == true ]]; then
        run_migrations "postgres"
        create_superuser "postgres"
    else
        run_migrations "$SERVER"
        create_superuser "$SERVER"
    fi
    
    echo -e "${GREEN}✅ Проект успешно запущен!${NC}"
    echo ""
    echo -e "${BLUE}📍 Доступные URL:${NC}"
    
    if [[ "$WITH_NGINX" == true ]]; then
        echo "   🌐 Веб-сайт: http://localhost"
        echo "   📊 Админка: http://localhost/admin/"
    else
        echo "   🌐 Веб-сайт: http://localhost:8000"
        echo "   📊 Админка: http://localhost:8000/admin/"
    fi
    
    echo ""
    echo -e "${YELLOW}📋 Полезные команды:${NC}"
    echo "   Логи:           $0 --logs"
    echo "   Остановка:      $0 --down"
    echo "   Перезапуск:     $0 $SERVER --build"
    echo ""
    echo -e "${BLUE}🔍 Просмотр логов:${NC}"
    $COMPOSE_CMD $PROFILES logs -f
}

main "$@"
