from django.urls import path
from .views import AuthView,LoginView

urlpatterns = [
    path("user_register",AuthView.as_view(),name="user_register"),
    path("user_login",LoginView.as_view(),name="user_login")
    
    
]