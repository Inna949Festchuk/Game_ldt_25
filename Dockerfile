# Используем официальный образ Python на базе Debian
FROM python:3.11-slim-bullseye

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    netcat \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint.sh с правильными правами доступа в корневую директорию
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Копируем проект
COPY ./app .

# Создаем пользователя без привилегий root
RUN useradd -m appuser && chown -R appuser:appuser /app

USER appuser

# Запускаем скрипт инициализации из корневой директории
ENTRYPOINT ["/entrypoint.sh"]