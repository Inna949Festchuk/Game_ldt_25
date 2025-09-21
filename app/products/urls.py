from django.urls import path
from . import views

urlpatterns = [
    path('import-excel/', views.import_excel_api, name='import-excel'),
    path('import-status/<str:task_id>/', views.import_status_api, name='import-status'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/generate-content/', views.generate_content_api, name='generate-content'),
]