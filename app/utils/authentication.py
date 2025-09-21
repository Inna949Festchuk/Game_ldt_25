from rest_framework import authentication
from rest_framework import exceptions
import requests

class ExternalServiceAuthentication(authentication.BaseAuthentication):
    """Аутентификация через внешний сервис"""
    
    def authenticate(self, request):
        # В реальной реализации здесь будет обращение к внешнему сервису
        # Для имитации возвращаем тестовый токен и пользователя
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        # Имитация проверки токена
        if token == 'test-token-123':
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='external_service_user',
                defaults={'is_active': True}
            )
            return (user, token)
        
        raise exceptions.AuthenticationFailed('Неверный токен аутентификации')

def get_external_token():
    """
    Функция для получения токена из внешнего сервиса
    В реальной реализации будет делать запрос к внешнему сервису
    """
    # Заглушка для демонстрации
    return "test-token-123"