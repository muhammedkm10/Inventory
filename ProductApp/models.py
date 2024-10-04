from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    description = models.TextField()
    stock = models.IntegerField()