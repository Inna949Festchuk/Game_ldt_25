# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /app/

# Собираем статические файлы Django с одновременной очисткой прежних статических файлов
RUN python manage.py collectstatic --noinput --clear 

# Создаем и применяем миграции
# RUN python manage.py makemigrations && python manage.py migrate

# Открываем порт, на котором будет работать Gunicorn
EXPOSE 8000

# Создаем и применяем миграции. Запускаем Gunicorn
CMD sh -c "python manage.py makemigrations && \
        python manage.py migrate && \
        gunicorn nerpa.wsgi:application --bind 0.0.0.0:8000"
# CMD ["gunicorn", "nerpa.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]