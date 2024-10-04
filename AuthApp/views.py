from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Create your views here.



# Registraion View
class AuthView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()  
            return Response({"data": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Login view
class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email = email,password = password)
        serailizer = TokenObtainPairSerializer(data= request.data)
        if user  and serailizer.is_valid():
            return Response({"token":serailizer.validated_data},status=status.HTTP_200_OK)
        return Response({"error":"enter valid credentials ,email and password"},status=status.HTTP_400_BAD_REQUEST)