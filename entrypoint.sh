#!/bin/sh

set -e  # Прерывать выполнение при любой ошибке

echo "Ожидание PostgreSQL..."
max_retries=30
retry_count=0

while ! nc -z db 5432; do
    retry_count=$((retry_count+1))
    if [ $retry_count -ge $max_retries ]; then
        echo "Не удалось подключиться к PostgreSQL после $max_retries попыток"
        exit 1
    fi
    echo "Попытка $retry_count из $max_retries: PostgreSQL недоступен, ждем..."
    sleep 2
done
echo "PostgreSQL доступен!"

# Выполнение миграций
echo "Применение миграций базы данных..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput --clear

# Запуск сервера
echo "Запуск сервера..."
exec "$@"