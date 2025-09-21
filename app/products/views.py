from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.core.cache import cache
from celery.result import AsyncResult

from .models import Product
from .serializers import ProductSerializer
from .tasks import import_from_excel
from utils.authentication import ExternalServiceAuthentication


@api_view(['POST'])
@authentication_classes([ExternalServiceAuthentication])
def import_excel_api(request):
    """API для импорта данных из Excel по URL"""
    excel_url = request.data.get('excel_url')
    
    if not excel_url:
        return Response(
            {'error': 'Не предоставлен URL Excel файла'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Запуск задачи Celery
    task = import_from_excel.delay(excel_url)
    
    return Response({
        'task_id': task.id,
        'message': 'Задача импорта запущена',
        'status_endpoint': f'/api/import-status/{task.id}/'
    }, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@authentication_classes([ExternalServiceAuthentication])
def import_status_api(request, task_id):
    """API для проверки статуса импорта"""
    task_result = AsyncResult(task_id)
    progress = cache.get(f'import_progress_{task_id}', 0)
    result = cache.get(f'import_result_{task_id}')
    
    response_data = {
        'task_id': task_id,
        'status': task_result.status,
        'progress': progress,
    }
    
    if result:
        response_data['result'] = result
    
    if task_result.status == 'FAILURE':
        response_data['error'] = str(task_result.result)
    
    return Response(response_data)

class ProductDetailView(RetrieveAPIView):
    """API для получения информации о продукте по slug"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    authentication_classes = [ExternalServiceAuthentication]

@api_view(['POST'])
@authentication_classes([ExternalServiceAuthentication])
def generate_content_api(request, slug):
    """API для генерации контента с помощью нейронной сети (заглушка)"""
    try:
        product = Product.objects.get(slug=slug)
        
        # Заглушка для нейронной сети
        # В реальной реализации здесь будет вызов нейронной сети
        generated_content = f"Сгенерированный контент для продукта {product.name}. Ссылки: {', '.join(product.links)}"
        
        product.content = generated_content
        product.save()
        
        return Response({
            'status': 'success',
            'message': 'Контент успешно сгенерирован',
            'content': generated_content
        })
    
    except Product.DoesNotExist:
        return Response(
            {'error': 'Продукт не найден'}, 
            status=status.HTTP_404_NOT_FOUND
        )
