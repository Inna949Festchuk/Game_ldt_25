# Game_ldt_25
## Бэкэнд для игры 

## Проект включает:

- Django с REST Framework
- PostgreSQL базу данных
- Celery для асинхронных задач
- Redis как брокер сообщений
- Nginx для обслуживания статических файлов
- Аутентификацию через внешний сервис
- API для импорта данных из Excel
- Автоматическое создание slug полей
- API для получения информации о продуктах

Все компоненты работают в Docker контейнерах, что обеспечивает изоляцию и простоту развертывания.

## Структура Django REST проекта с Docker, PostgreSQL, Celery и Redis

```
cd game_ldt_25/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
|   |   └── celery.py
│   ├── products/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── authentication.py
│   ├── manage.py
│   └── requirements.txt
├── nginx/
│   ├── nginx.conf
│   └── ssl/
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
└── .env
```

## Запуск проекта

1. Клонируйте и настройте проект:
```bash
git clone <репозиторий>
cd game_ldt_25
```

2. Создайте SSL сертификаты для Nginx:
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/server.key \
    -out nginx/ssl/server.crt \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=Company/CN=localhost"
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

4. Примените миграции базы данных (если не сработало автоматически):
```bash
docker-compose exec web python manage.py migrate
```

5. Создайте суперпользователя для доступа к админке:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Использование API

1. Импорт данных из Excel:
```bash
curl -X POST -H "Authorization: Bearer test-token-123" \
  -H "Content-Type: application/json" \
  -d '{"excel_url": "https://docs.google.com/spreadsheets/d/11FjKpCsaqnNWuzq3xmJcRiVOV3dxyA6l/export?format=xlsx"}' \
  http://localhost/api/import-excel/
```

2. Проверка статуса импорта:
```bash
curl -H "Authorization: Bearer test-token-123" \
  http://localhost/api/import-status/<task_id>/
```

3. Получение информации о продукте:
```bash
curl -H "Authorization: Bearer test-token-123" \
  http://localhost/api/products/<slug-продукта>/
```

4. Генерация контента для продукта:
```bash
curl -X POST -H "Authorization: Bearer test-token-123" \
  http://localhost/api/products/<slug-продукта>/generate-content/
```

Этот проект предоставляет полную основу для вашего Django REST API с использованием современных технологий и лучших практик. Все компоненты настроены для работы в контейнерах Docker, что обеспечивает простоту развертывания и масштабирования.