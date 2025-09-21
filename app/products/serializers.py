from rest_framework import serializers
from .models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типа продукта"""
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта"""
    product_types = ProductTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'content', 'links', 'product_types', 'created_at', 'updated_at']
        read_only_fields = ['slug']  # Slug заполняется автоматически