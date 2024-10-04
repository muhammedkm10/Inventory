from rest_framework import serializers
from .models import Products

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Products
        fields  = "__all__"
    # validating the product name
    def validate_name(self,value):
        if not value:
            raise serializers.ValidationError("Name is required")
        # for adding the product
        if self.instance:
            if Products.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("The Product is already present")
        else:
            if Products.objects.filter(name=value).exists():
                raise serializers.ValidationError("The Product is already present")
        return value
    # validating the stock
    def validate_stock(self,value):
        if not isinstance(value,(int,float)):
            raise serializers.ValidationError("The field should be a number")
        if value < 0:
            raise serializers.ValidationError("The Stock should be greater than or equal to zero")
        return value
    
    #  validating the description
    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value
    
    
    
        