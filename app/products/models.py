from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

class ProductType(models.Model):
    """Модель типа продукта"""
    name = models.CharField(max_length=255, verbose_name="Название типа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        verbose_name = "Тип продукта"
        verbose_name_plural = "Типы продуктов"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    content = models.TextField(blank=True, verbose_name="Контент")
    links = models.JSONField(default=list, verbose_name="Ссылки")
    product_types = models.ManyToManyField(ProductType, related_name="products", verbose_name="Типы продуктов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    
    def __str__(self):
        return self.name

# Сигнал для автоматического создания slug при сохранении продукта
@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, **kwargs):
    """Автоматическое создание slug из названия продукта"""
    if not instance.slug:
        instance.slug = slugify(instance.name)