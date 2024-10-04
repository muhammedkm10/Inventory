from django.urls import path
from .views import AuthView

urlpatterns = [
    path("user_register",AuthView.as_view())
    path("user_login",AuthView.as_view())
    
    
]