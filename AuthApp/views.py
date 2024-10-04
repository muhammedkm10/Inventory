from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import logging
# Create your views here.

logger = logging.getLogger("AuthApp")

# Registraion View
class AuthView(APIView):
    def post(self, request):
        logger.info("Received request to create a new user.")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User created successfully: {serializer.data['email']}")
            return Response({"data": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"User creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class LoginView(APIView):
    def post(self, request):
        logger.info("Received request for user login.")
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        serializer = TokenObtainPairSerializer(data=request.data)

        if user and serializer.is_valid():
            logger.info(f"User logged in successfully: {email}")
            return Response({"token": serializer.validated_data}, status=status.HTTP_200_OK)
        logger.warning("Login failed: Invalid credentials provided.")
        return Response({"error": "Enter valid credentials, email and password"}, status=status.HTTP_400_BAD_REQUEST)