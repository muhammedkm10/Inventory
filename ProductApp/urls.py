from django.urls import path


urlpatterns = [
    path('product_management',ProductManagment.as_view())
    
]