import os
from celery import Celery

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создание экземпляра объекта Celery
app = Celery('core')

# Загрузка настроек из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех зарегистрированных приложений Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """Простая задача для отладки"""
    print(f'Request: {self.request!r}')