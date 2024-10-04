from django.urls import path
from .views import ProductManagment


urlpatterns = [
    path('product_management',ProductManagment.as_view()),
    path('product_management/<str:item_id>',ProductManagment.as_view())
    
    
]

