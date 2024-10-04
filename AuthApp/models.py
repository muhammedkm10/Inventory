from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username =  models.CharField( max_length=50,unique=False, null=True, blank=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    
    