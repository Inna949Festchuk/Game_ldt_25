from django.contrib import admin
from .models import ProductType, Product

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """Административный интерфейс для типа продукта"""
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административный интерфейс для продукта"""
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug', 'content')
    list_filter = ('product_types', 'created_at', 'updated_at')
    filter_horizontal = ('product_types',)
    readonly_fields = ('slug',)
    
    def save_model(self, request, obj, form, change):
        """Автоматическое создание slug при сохранении через админку"""
        if not obj.slug:
            from django.utils.text import slugify
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)