import pandas as pd
from celery import shared_task
from django.core.cache import cache
from .models import Product, ProductType

from celery import shared_task
from time import sleep

# @shared_task
# def test_task():
#     """Тестовая задача для проверки работы Celery"""
#     sleep(5)
#     return "Тестовая задача выполнена успешно!"

@shared_task(bind=True)
def import_from_excel(self, excel_url):
    """Задача Celery для импорта данных из Excel"""
    try:
        # Чтение Excel файла
        df = pd.read_excel(excel_url)
        
        # Кэширование прогресса импорта
        cache.set(f'import_progress_{self.request.id}', 0)
        
        total_rows = len(df)
        processed = 0
        
        for index, row in df.iterrows():
            # Обработка типа продукта
            type_name = row.get('Тип продукта', '')
            if type_name:
                product_type, created = ProductType.objects.get_or_create(name=type_name)
            
            # Обработка продукта
            product_name = row.get('Продукт', '')
            links = row.get('Ссылки', '').split(',') if row.get('Ссылки') else []
            
            if product_name:
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'links': links}
                )
                
                if type_name and product_type:
                    product.product_types.add(product_type)
            
            # Обновление прогресса
            processed += 1
            progress = int((processed / total_rows) * 100)
            cache.set(f'import_progress_{self.request.id}', progress)
        
        cache.set(f'import_result_{self.request.id}', 'Импорт завершен успешно!')
        return "Импорт завершен успешно!"
    
    except Exception as e:
        cache.set(f'import_result_{self.request.id}', f'Ошибка: {str(e)}')
        raise self.retry(exc=e, countdown=60)