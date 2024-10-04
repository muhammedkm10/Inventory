from django.urls import path
from .views import AuthView,LoginView

urlpatterns = [
    path("user_register",AuthView.as_view()),
    path("user_login",LoginView.as_view())
    
    
]