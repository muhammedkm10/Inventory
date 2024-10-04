from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
            'email': {'required': True},
        }
    
    def validate_username(self, value):
        print(value,"username")
        if not value:
            raise serializers.ValidationError("Username is required")
        if not value.isalpha():
            raise serializers.ValidationError("Username should contain only alphabetic characters")
        return value
    
    def validate_email(self,value):
        if CustomUser.objects.filter(email = value).exists():
            raise serializers.ValidationError("Emails is already exists")
        return value
    
    
    
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'] ,
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    
    
        
    